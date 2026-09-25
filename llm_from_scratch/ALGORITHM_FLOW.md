"""
Transformer Forward & Backward Flow: Step-by-Step with Why

This document maps the exact control flow inside tiny_transformer.py and small_transformer.py
(read: future TinyTransformer) so it reads like a directed flowchart.

For every major function, we show:
1. Data shape transformations
2. The exact matrix/ops applied
3. Why that operation exists (what problem it solves)
4. What would break without it

The goal is to turn "I ran cross_entropy_loss(logits, y)" into:
   "Here is what happens line-by-line, why the indices align, and how gradients flow back up."
"""

# ============================================================
# SECTION 0: The Data Pipeline (what arrives at the model)
# ============================================================

STEP 0.1 — Corpus -> Token ID list
-----------------------------------
Input:  raw string
Output: `ids`, a Python list of integers

Code:
    corpus = "the quick brown fox jumps over the lazy dog " * 8
    vocab = {"<pad>": 0, "<unk>": 1}
    for token in corpus.split():
        if token not in vocab:
            vocab[token] = len(vocab)
    rev = {i: t for t, i in vocab.items()}
    ids = [vocab.get(t, 1) for t in corpus.split()]

Why:
    The model cannot read words. It reads numbers. This step translates
    human language into a fixed-size lookup index.

What breaks without it:
    You cannot do matrix math on strings.

---

STEP 0.2 — Train into X / Y pairs
---------------------------------
Input: `ids`, `seq_len=50`
Output: every consecutive window of 50 tokens as `(X, Y)`

Code:
    for i in range(0, len(ids) - seq_len, seq_len):
        chunk = ids[i:i + seq_len]
        X = np.array(chunk[:-1], dtype=np.int64).reshape(1, -1)
        y = np.array(chunk[1:], dtype=np.int64)

Shape:
    ids has length ~400
    chunk has length 50
    X  -> [1, 49]
    y  -> [49]

Why:
    Language is modeled one token at a time. Given the first 49 tokens,
    predict the 50th.

What breaks without it:
    The model learns nothing; there is no supervised signal.

---

# ============================================================
# SECTION 1: Forward Pass (one training step)
# ============================================================

STEP 1.1 — Embedding Lookup
----------------------------
Input:  X (batch of token ids)
Output: `emb`, [batch, seq_len, d_model] flat vectors

Code:
    M = np.random.randn(vocab_size, E) * sqrt(2/E)
    emb = M[X, :]                 # gather rows of M
    emb = emb + pe[:X.shape[1], :]

Shape math:
    M        -> [vocab_size, E]      = [20, 8]
    X        -> [1, 49]             (one hot-ish id per row)
    emb      -> [1, 49, 8]

Why:
    Every token needs a dense vector that the model can multiply by matrices.
    You cannot multiply a word by a matrix; you multiply its embedding vector.

Why not just indices?
    If you used raw integers, multiplying by `[vocab_size, d_model]` would
    give a diagonal matrix (identity). The model would never learn
    non-trivial relationships.

What breaks without it:
    Backprop has no gradients to get; the model is just doing integer math.

---

STEP 1.2 — Self-Attention (Multi-Head)
---------------------------------------
Input:  emb, [batch, seq_len, d_model]
Output: attn_out, [batch, seq_len, d_model]

1.1 Project to Q, K, V
    query = emb @ W_q
    key   = emb @ W_k
    value = emb @ W_v

    Reshape into heads:
    query = query.reshape(B, T, n_heads, d_k)   # [1, 49, 2, 4]

Why three separate matrices?
    If W_q == W_k == W_v, every dimension of the query is "what I look for"
    *and* "what I match against." The model can only represent one
    relationship type (e.g., identity) and cannot simultaneously encode
    syntax and entity type.

1.2 Scaled Dot-Product
    raw_scores = query @ key.transpose(0,1,3,2)   # [1,49,2,2,4]
    raw_scores = raw_scores * (1 / sqrt(d_k))      # [1,49,2,2,4]

    Why divide by sqrt(d_k)?
    query @ key is a sum of d_k products. When d_k is large, the dot
    product grows linearly and softmax saturates (one prob ≈ 1, others ≈ 0).
    During training, this means one gradient dominates and others die.

    What breaks without it?
    With d_k=4, sqrt=2, drops are mild.
    With d_k=64, sqrt=8, raw scores are ~8x smaller.
    Without scaling, a 64-dim model is numerically unstable.

1.3 Softmax
    scores = softmax(raw_scores, axis=-2)   # [1,49,2,2,4]

    Why softmax?
    We need a probability distribution: "how much attention do I pay to
    each other token?" Softmax enforces positivity and sums to 1.

    What breaks without it?
    Raw scores could be negative; they do not form a budget.
    The model could assign "negative attention" which is undefined.

1.4 Weighted Sum (Value)
    attn = scores @ value   # [1,49,2,2,4]
    attn = attn.reshape(B, T, d_model)   # [1,49,8]

What breaks without it?
    No way to produce a context-aware output.

1.5 Output Projection
    out = attn @ W_out + b_out   # [1,49,8]

Why final W_out?
    The attention head mixes queries at dimension `d_k` but the model needs
    the result at full `d_model`. W_out is a learned linear map.

    What breaks without it?
    The output dimensionality mismatch.

---

STEP 1.3 — Feed-Forward Network
--------------------------------
Input:  out from attention, [1, 49, 8]
Output: ffn_out, [1, 49, 8]

Code:
    z1 = w1 @ ffn_out + b1          # -> [1, 49, 16]
    a1 = z1 * mask(z1>0)            # ReLU, in-place
    z2 = w2 @ a1 + b2               # -> [1, 49, 8]

Why a 2-layer MLP instead of one layer?
    A single linear layer is just another projection: y = x @ M.
    Two layers with ReLU add a nonlinearity: y = x @ M2 + b2  where
    (x @ M1)_ReLU has already been computed.
    This gives the model the ability to model "is x in this region?"
    (via ReLU) and then "transform that region" (via the second layer).

If one layer:
    You cannot learn piecewise-linear functions that depend on
    thresholds. Every function is a hyperplane.
    With two layers + ReLU, you can approximate any piecewise-linear
    function with sufficient width.

What breaks without it?
    The output from attention is already a linear function of the inputs.
    A second linear layer is redundant unless you add nonlinearity.
    Without ReLU, the model is just one big linear system and you
    cannot fit complex language patterns.

---

STEP 1.4 — Vocabulary Prediction
---------------------------------
Input:  ffn_out, [1, 49, 8]
Output: logits, [1, 49, vocab_size]

Code:
    logits = ffn_out @ W_logits + b_logits

    W_logits -> [d_model, vocab_size]   = [8, 7]
    b_logits -> [vocab_size]            = [7]

Why vocabulary-size output, not 2 (for two words)?
    We treat each position as "next token prediction" over the full
    vocabulary. This is the standard language-modeling objective.

If we had only 2 classes:
    The model could not distinguish "cat" from "dog" from "the."
    It would be forced into a binary decision and memorization would
    be impossible with this tiny dataset.

---

STEP 1.5 — Loss
----------------
Input:  logits, [1, 49, vocab_size]; y, [49]
Output: scalar loss

Code:
    probs      = softmax(logits, axis=-1)   # [1,49,7] -> valid distribution
    ce_i[i]    = -log(probs[0, i, y[i]])   # per-position
    loss       = mean(ce_i)

Why per-position and not sequence-level?
    We want the model to be good at every step, not just every sequence.
    Averaging per-position gives us more gradient signals per batch.

What breaks without it?
    No training signal.

---

# ============================================================
# SECTION 2: Backward Pass (one training step)
# ============================================================

The backward pass follows reverse order of forward, differentiating
each operation and accumulating gradients.

NOTE: In tiny_transformer.py the backward pass is split:
    FFNN.backward() handles its own matrices.
    MultiHeadAttention.backward() handles its own.
    There is no end-to-end backprop through the whole Transformer block
    (i.e., no TransformerBlock class that chains attn+ffn+backprop).

To make the Backward Flow concrete, we show the standard Transformer
backprop as it *would* look if we wrote it manually.

---

STEP 2.1 — Loss Gradient w.r.t. Logits
--------------------------------------
Input:  logits, [1,49,7]
Output: d_logits, [1,49,7]

Code:
    probs = softmax(logits, axis=-1)
    d_logits = probs             # gradient of cross-entropy w.r.t. logits
    d_logits [np.arange(1), np.arange(49), y] -= 1

    `probs` because d(CE)/d(logits) = 1 - p_true = p_true - 0 = probs.
    Then subtract 1 at the true-token entries so E[d_logits] == 0,
    which stabilizes training.

Why:
    The loss wants to push logits[true_token] up and others down.
    The derivative is exactly the "prediction minus one-hot target."
    This is the exact gradient of cross-entropy with softmax.

---

STEP 2.2 — Logits -> FFN Gradient
----------------------------------
Input:  d_logits, [1,49,vocab_size]
Output: d_ffn, [1,49,d_model]

Code:
    d_ffn = d_logits @ W_logits.T

Why matrix multiplication with W_logits.T?
    Backprop through y = x @ W + b gives dy/dx = dy/dy @ W.T.
    Since logits are the output of the FFN, the gradient flows back
    as a matrix product.

What breaks without it?
    You cannot attribute the loss gradient to the right layer.

---

STEP 2.3 — FFN Backward
------------------------
Input:  d_ffn, [1,49,8]; cache (a, z1, a1, z2)
Outputs: gradients for W1, b1, W2, b2

Forward:   z1 = a @ W1 + b1
            a1 = ReLU(z1)
            z2 = a1 @ W2 + b2

Gradient chain:
    d2/db2 = sum(d_ffn, axis=0)              # -> [8]
    d2/dW2 = a1.T @ d_ffn                     # -> [16,49]

    dz2 = d_ffn                               # shape [1,49,8]
    z1 = cache["z1"]                          # [1,49,8]
    da1 = dz2 * (z1 > 0)                      # mask where ReLU was active
    dz1 = da1 @ W2.T                          # -> [1,49,16]
    db1 = sum(da1, axis=0)                    # -> [16]
    dW1 = a.T @ da1                           # -> [4,49]

Why mask with (z1 > 0)?
    ReLU derivative is 1 if z1 > 0, else 0.
    Only the active units contribute to the gradient; dead units
    (z1 <= 0) have zero derivative, so the weights feeding them
    do not change.

What breaks without it?
    Gradients would leak through dead ReLUs, effectively trying to
    un-kill a dead unit. In practice, this just means learning noise,
    but the math is wrong.

---

STEP 2.4 — FFN -> Attention Backward
--------------------------------------
Input:  gradient from D_FFN with respect to attention output
Output: gradient w.r.t. attention scores / values
(This step is deliberately skipped in tiny_transformer.py because
 there is no TransformerBlock.backward() that wires them.)

In a full backward pass, you would compute:
    da_attn = d_ffn @ W_out.T
    Then feed da_attn into the same backward logic as Step 2.3,
    starting from the attention output.

---

STEP 2.5 — Attention Backward (conceptual)
------------------------------------------
If wired: each attention weight `w_ij` is a function of
  q_i, k_j, v_j.
By the chain rule:
    d Loss / d q_i = (dL/d attn_out) @ W_out.T @ (soft_i)
    dL/d attn_out is the vector of attention gradients coming from
    the layer after (FFN or next layer).
    W_out.T maps back to the d_model space.
    soft_i is the attention probability row for token i.

For each head:
    dQ, dK, dV = full backprop through attention formula.
    The formula (from *Attention Is All You Need* Appendix B) is:
        dAttn = (soft_i^T @ d_output)  [broadcast to all tokens]
        dV = dAttn
        dK = (1/sqrt(d_k)) * dAttn @ (q_i^T @ d_output)
        dQ = (1/sqrt(d_k)) * dAttn @ (v_j^T @ d_output)

In code, that translates to:
    dAttn = (soft_i^T @ d_output)
    dV = dAttn
    dK += soft_i @ (v_j.T @ d_output)
    dQ += soft_i @ (k_j.T @ d_output)

What breaks without it?
    You cannot update W_q, W_k, W_v, W_out based on the loss.

---

# ============================================================
# SECTION 3: The Complete Forward-Backward Cycle
# ============================================================

Forward:
    1.  Tokenize    -> ids
    2.  Embed + Pos -> emb [1,49,8]
    3.  Attn         -> out  [1,49,8]
    4.  FFN          -> z    [1,49,8]
    5.  Logits       -> logits [1,49,7]
    6.  Loss         -> scalar

Backward:
    7.  dLoss/dLogit -> dlogits  [1,49,7]
    8.  dLogit/dFFN   -> dN       [1,49,8]
    9.  dFFN/dW1/b1   -> update   (back to item 4)
   10.  dN/dW_out    -> update    (back to item 3)
   11.  (via backprop) -> update  W_k, W_v, W_q, W_out

What this cycle achieves:
    After ~100 epochs, the model has adjusted every matrix parameter
    so that the predicted next token matches the true next token.
    Because of residuals and LayerNorm, the gradients stay in the
    right magnitude throughout the 25-layer-equivalent depth.

---

# ============================================================
# SECTION 4: Why the Residual + LayerNorm + FFN Pattern
# ============================================================

In a real Transformer, each position is:
    x = x + LayerNorm(Attention(x) + LayerNorm(FFN(x)))

Or in our tiny_transformer.py:
    emb = M[inp, :] + pe[pos, :]     # embedding + positional
    z = ffn.forward(emb)             # FFN only
    logits = z @ W_logits + b_logits

Because we skipped attention blocks (they are in MultiHeadAttention
but not wired into a TransformerBlock), the "knows about itself"
pattern is only present implicitly.

In a full pipeline, why `x = x + ...`?
    Identity: if the optimal transformation is zero, the network can
    set all extra weights to zero and pass the signal through.
    Without residual, if you want FFN to do nothing, you must learn
    weights that multiply to nearly zero, which is unstable.

    LayerNorm before each sub-layer ensures the input distribution
    stays stable depth-wise.

---

# ============================================================
# SECTION 5: Why Sinusoidal Positions, Not Learned
# ============================================================

We use:
    pe[pos, 2i]   = sin(pos / 10000^{2i/d})
    pe[pos, 2i+1] = cos(pos / 10000^{2i/d})

Why:
    1. Generalization: learned embedding of position is a lookup table.
       For a sequence of length 50, you store 50 vectors.
       Longer sequences (55, 60) have no representation and you must
       either truncate or pre-compute.
       Sinusoidal positions compute any `pos` on the fly.
    2. Relative position:
       sin(pos + k) can be expressed as sin(pos)cos(k) + cos(pos)sin(k),
       which is a linear function of [sin(pos), cos(pos)].
       This means attention can learn "distance +2" by a linear probe.
    3. No extra parameters.

What breaks without it:
    Longer-than-trained sequences fail.

---

# ============================================================
# SECTION 6: Common Failure Modes
# ============================================================

| Failure | Symptom | Cause |
|---------|---------|-------|
| Cross-entropy IndexError | `IndexError: index 1 is out of bounds` | `logits` has too few classes (e.g. `[1,1]` instead of `[1,3]`) |
| NaN / Inf loss | Loss explodes | No LayerNorm, or lr too high, or d_k too large without scale |
| Attention is uniform | All head outputs same | W_q, W_k, W_v initialized identically or too small |
| FFN does nothing | Loss stuck | ReLU kills all inputs (zero initialization of W1) |
| Positional drift | Model confuses early/late tokens | Insufficient positional dimensions, or no positional encoding at all |

---

# ============================================================
# SECTION 7: The Algorithm as Pseudocode (Clean Flow)
# ============================================================

```
ALGORITHM TinyTransformer
    INPUT  corpus, seq_len, vocab_size, d_model, n_heads, epochs
    OUTPUT  rev (reverse vocabulary)

    vocab, rev = BUILD_VOCAB(corpus)
    ids = [vocab.get(t, 1) for t in corpus.split()]

    M = RANDOM_NORMAL([vocab_size, d_model]) * SQRT(2 / d_model)
    pe = BUILD_POSITIONAL(seq_steps=500, dim=d_model)

    W_logits = RANDOM_NORMAL([d_model, vocab_size]) * SQRT(2 / d_model)
    b_logits = ZERO([vocab_size])

    for epoch = 1 to epochs:
        for i = 0 to len(ids)-seq_len step seq_len:
            chunk = ids[i : i+seq_len]
            X = chunk[0:seq_len-1] reshaped to [1, seq_len-1]
            y = chunk[1:seq_len]

            # FORWARD
            emb = EMB(X) + PE[:len(X[0])]         # [1,T,d_model]
            attn = ATTENTION(emb)                  # [1,T,d_model]
            ffn = FFN(attn)                        # [1,T,d_model]
            logits = ffn @ W_logits + b_logits     # [1,T,vocab_size]

            # BACKWARD (manual)
            loss = CROSS_ENTROPY(logits, y)
            dlogits = PROBS(logits)
            dlogits[0, np.arange(T), y] -= 1
            dN = dlogits @ W_logits.T               # [1,T,d_model]

            # FFN backward
            d2 = dN
            db2 = SUM(d2, axis=0)
            da1 = d2 * MASK(z1 > 0)
            dW2 = a1.T @ d2
            dz1 = da1 @ W2.T
            db1 = SUM(da1, axis=0)
            dW1 = a.T @ da1

            # Attention backward (omitted in current code)
            dW_out, dW_v, dW_q = ATTENTION_BACKPROP(d2, scores, q, k, v)

            # SGD step
            W1 -= lr * dW1
            b1 -= lr * db1
            W2 -= lr * dW2
            b2 -= lr * db2
            W_logits -= lr * (dN @ X.T)
            W_out -= lr * (d2 @ attn.T)

    RETURN rev
```

END ALGORITHM
