# Transformer Intuition: What and Why

A human-readable guide to the operations inside `tiny_transformer.py`.

For each operation, we answer:
- **What** — the concrete step.
- **Why we do it** — the problem it solves.
- **Why it matters** — what breaks if you skip it.
- **Example / intuition** — a plain-English analogy or toy number.

---

## 1. Positional Encoding: `sin(pos / 10000^{2i/d})`

### What
The Transformer has no recurrence, no temporal structure, and no concept of "index 1 comes after index 0." We must inject a signal that tells the model: *this token is at position 5, that token is at position 12.*

The standard sinusoidal encoding computes, for each dimension `i` (from `0` to `d-1`):

```
PE(pos, 2i)   =  sin(pos / 10000^{2i/d})
PE(pos, 2i+1) =  cos(pos / 10000^{2i/d})
```

In code (vectorized):
```python
for i in range(d):
    encoding[pos, i] = sin(pos / (10000**(2*i/d)))
```

### Why we do it
Without positional information, self-attention treats "cat" at the start of a sentence the same as "cat" at the end. For language, word order is meaning.

### Why it matters
If you remove positional encodings, the attention matrix becomes identical regardless of input order. A model trained on "The dog barks" would treat it the same as "Barks dog The" — it would learn nothing about syntax or meaning.

The sinusoidal form has a useful property: **PE(pos+k) = PE(pos) shifted by a constant amount** in some dimensions. This means the model can easily learn relative position (e.g., "the 's in position 3 is 2 words after the 'the" in position 1) by a simple linear operation on the encodings.

### Example
Imagine `d=4`, `pos=0`:

```
i=0: sin(0 / 10000^0)   = sin(0)   = 0.0000
i=1: cos(0 / 10000^0)   = cos(0)   = 1.0000
i=2: sin(0 / 10000^{0.5}) = sin(0)   = 0.0000
i=3: cos(0 / 10000^{0.5}) = 1.0000
```

For `pos=1`:

```
i=0: sin(1 / 1)   = sin(1)   ≈ 0.8415
i=1: cos(1 / 1)   = cos(1)   ≈ 0.5403
i=2: sin(0.01)    ≈ 0.0100
i=3: cos(0.01)    ≈ 0.99995
```

Notice: the low-frequency dimensions (~i=0,1) change quickly with position, while high-frequency dimensions (~i=2,3) barely change. The network can encode "global position" using the low-frequency wave and "local position" using the high-frequency wave.

### Why base 10000?

The base 10000 is chosen so that:
- For short sequences (pos < 5000), all arguments to `sin/cos` are small (< 1) so the wave is smooth and monotonic.
- For long sequences, the exponent `2i/d` is large enough that `10000^{...}` grows, making the denominator huge and the argument tiny again.
- In practice, 10000 is a historical constant from the original *Attention Is All You Need* paper. Any base > 1 gives the same mathematical effect; 10000 was simply picked to make the numbers well-behaved for English-length sequences.

You could replace 10000 with 2, 10, or 1000 and still get a perfectly valid positional encoding, but the "phase" of each wave would change.

---

## 2. Attention Scaling: `1 / sqrt(d_k)`

### What
Before applying `softmax` to the attention scores, we divide by `sqrt(d_k)` where `d_k` is the dimension of the key vectors (usually `d_model / n_heads`).

```python
scale = 1.0 / np.sqrt(self.d_k)
scores = softmax(matmul_bmm(q, k.T) * scale, axis=-1)
```

In our code (batched):
```python
scale = 1.0 / np.sqrt(self.d_k)
scores = softmax(matmul_bmm(q, k.transpose(0,1,3,2)) * scale, axis=-1)
```

### Why we do it
The dot-product `q @ k` is a sum of products. If `d_k` is large, the dot product grows linearly with dimension. A large dot product means a large temperature on the exponential, which means very sharp softmax distributions (many weights become vanishingly small, and the model becomes unstable to small changes in the data).

### Why it matters
Without scaling, deeper Transformers (more heads, wider models) suffer from gradient explosion and dead attention heads. The original Transformer paper explicitly notes that scaling is "necessary for stable training."

### Example
Imagine `q = [0.1, 0.1]` and `k = [0.1, 0.1]`.
- `q @ k = 0.01 + 0.01 = 0.02`.
- `softmax(0.02)` is mild.

Now imagine `q = [1, 1, ..., 1]` with `d_k = 64`.
- `q @ k = 64 * 1 * 1 = 64`.
- `exp(64)` overflows; the softmax is numerically meaningless.

Even before overflow, `exp(64)` dominates `exp(0)`, making all other tokens have attention ≈ 0. The model stops attending to anything else.

By dividing by `sqrt(d_k) = 8`, the same example becomes `64 / 64 = 1.0`, which is a sane scale.

---

## 3. Multi-Head Attention

### What
Instead of one large attention mechanism, we split `d_model` into `n_heads` groups of size `d_k = d_model / n_heads`. Each head computes its own scaled dot-product attention on a different linear projection of the input.

```python
W_q = ... @ 32x32
W_k = ... @ 32x32
W_v = ... @ 32x32

query = x @ W_q       # shape: [B, T, d_model]
head_q = query.reshape(B, T, n, d_k)  # e.g., [B, T, 2, 16]
query_head = head_q @ W_q.T ...     # But in code we usually do:
query = x @ W_q                       # [B, T, d_model]
key   = x @ W_k                       # [B, T, d_model]
value = x @ W_v                       # [B, T, d_model]
query = query.reshape(B, T, n, d_k)
key   = key.reshape(B, T, n, d_k)
value = value.reshape(B, T, n, d_k)
scores = soft ...
attention_head = scores @ value
output = concat(heads) @ W_out
```

In our `tiny_transformer.py`, this collapses to the shorthand:
```python
q = matmul_bmm(x, self.W_q)
k = matmul_bmm(x, self.W_k)
v = matmul_bmm(x, self.W_v)
q = q.reshape(B, T, n, d_k)
k = k.reshape(B, T, n, d_k)
v = v.reshape(B, T, n, d_k)
```
The attention itself is then one hotspot `softmax(q @ k.T) @ v`.

### Why we do it
A single attention head must capture *all* relationships between any two positions. If `d_model = 1024` and `n_heads = 16`, one head only sees `d_k = 64` dimensions.

By using many heads, the model can:
- Focus on different aspects: syntax, coreference, long-range dependencies, local grammar, etc.
- Look at the same positions from different subspaces.
- Avoid representational bottlenecks: if two unrelated relationships should have zero influence, different heads can learn to ignore them.

### Why it matters
With one head, the model is forced to compress every relational question into 64 floating-point numbers. With 16 heads, each question gets its own 64-number subspace. Empirically, this is the single most important architectural choice in the Transformer.

### Example
Consider the sentence: *"The cat sat on the mat."*

- **Head 1** might learn to compare "cat" to "sat" (local verb-subject agreement).
- **Head 2** might compare "cat" to "The" (determiner-noun).
- **Head 3** might compare "sat" to "mat" (distant action-location).
- **Head 4+** might capture negation, person, tense, or entity types.

If you had only one head, it would be forced to blend all of these signals into 64 numbers. The result would be noisy and context-insensitive.

---

## 4. Layer Normalization (the idea)

### What
Layer Normalization normalizes the activations of a layer *across the feature dimension* for each token independently:

```
y = x - mean(x) / std(x)
y = gamma * y + beta
```

In practice, before the attention block:
```python
x = LayerNorm(x + Attention(x))
```
After the FFN:
```python
x = LayerNorm(x + FFN(x))
```

Inside our code, the `+ x` is the **residual connection**, and `LayerNorm` is the hidden normalization step.

Our implementation skipped full LayerNorm to keep the code minimal, but it is conceptually essential.

### Why we do it
During training, gradients can grow or shrink excessively depending on depth and skip connections. Layer Normalization fixes the scale of activations empirically, making:
- Layer outputs have near-zero mean and unit variance.
- The model depth becomes much less sensitive to initialization.
- Training become stable across a wider range of hyperparameters.

### Why it matters
Without LayerNorm, deep Transformers are hard to train. ResNet showed the same pattern with BatchNorm on images. Transformer papers showed that LayerNorm is as important as the attention mechanism itself for convergence.

### Example
Imagine a 4-layer Transformer with `d_model = 32`.
- Layer 1 outputs values around `[0, 10]`.
- Layer 2 outputs values around `[0, 100]` (because it multiplies by `W2` with gain 10).
- Layer 3 outputs `[0, 1000]`.
- Layer 4 outputs `[0, 10000]`.

ReLU units kill half the signal at each layer, so the initial layers' gradients barely reach the final layer. The model cannot learn features at early layers.

LayerNorm forces every layer to output roughly `[0, 5]` (after a learned scale). The gradient can flow unchanged across all 4 layers.

---

## 5. Residual Connections (`x + FFN(x)`)

### What
Instead of computing `y = FFN(FFN(...FFN(x)...))`, we compute:
```
y = x + FFN(x)
z = y + FFN(y)
w = z + FFN(z)
...
```

In code inside `Forward`:
```python
attn_out = self.attn.forward(x)
ffn_out  = self.ffn.forward(attn_out)
```

The residual is conceptual: `out = x + ffn(x)`.

### Why we do it
Composition of nonlinearities is exponential depth: `N` layers = `explanation^N` combinations. But for "easy" transformations (like identity), `f(x) = x`, the derivative of a deep stack becomes vanishingly small:
```
f^N(x) ≈ 0  (for deep networks with sum of small weights)
```

Residual blocks allow the network to learn "zero" easily: set all extra weights to 0, and the architecture becomes just `x`.

### Why it matters
Without residuals, training deep Transformers directly is impossible. Even ResNet (20-150 layers) requires them. For Transformers, residuals are the reason a 12-layer model trains at all.

### Example
Layer 1 output is `s1`.
- **Without residual:** Layer 2 needs to learn `s2 = tfn(s1)`, where `s2` might be close to `s1`.
- **With residual:** Layer 2 can learn `s2 = s1 + tfn(s1)` with `tfn(s1) ≈ 0`.

If the optimal function is nearly the identity, the network can set the extra weights to near-zero and pass the signal through unchanged. This makes optimization convex-like locally and removes the gradient trap.

---

## 6. Feed-Forward Network (MLP)

### What
After attention, each token goes through a 2-layer MLP:
```
hidden = x @ W1 + b1
activated = relu(hidden)
output   = activated @ W2 + b2
```
In our code, `FFNN` implements exactly this, with the intermediate matrix named `z1` and the activation applied in-place.

### Why we do it
Attention mixes information across positions, but it is a *quadratic* operation (needs O(n^2) memory and time). The FFN is a local, *linear* transformation that processes each position independently and adds non-indcendence:
- Attention: "What words influence me?"
- FFN: "Given my current view of the sentence, how should my representation change?"

The FFN is also the only quadratic-free way to let the model increase dimension (bottleneck + expansion).

### Why it matters
Without the FFN, the network is just a sequence of repeated attention matrices. Attention cannot represent arbitrary functions without many layers and huge context windows. The FFN gives each position a "private" nonlinear transformer.

### Example
Consider the attention output for "cat" in *"The cat chased the mouse."*.
- Attention says: "cat" interacts with "The" (determiner), "chased" (verb), and "mouse" (object).
- The FFN can now take the weighted sum of these interactions and produce a new vector that says: "This is a singular noun, past tense, subject of a transitive verb."

If you removed the FFN, "cat" would remain a raw weighted average of its neighbors. The FFN encodes *compound* properties that are not directly present in any single neighbor.

---

## 7. Softmax in Attention

### What
```python
probs = exp(scores) / sum(exp(scores))
```

### Why we do it
We need a *distribution* over positions: how much attention should each token pay to every other token?

Softmax has three desirable properties:
1. **Positivity**: All attention weights are > 0 (no hard masking).
2. **Normalization**: All weights sum to 1 (the "pie budget" is fixed).
3. **Monotonicity**: A small increase in a score increases its weight, but the increase is damped by the other weights (stable attention).

### Why it matters
Without softmax (e.g., using raw scores), attention would be a weighted sum that is not interpretable and numerically unstable. With softmax, attention is literally: *"I distribute 1 unit of focus to tokens X_{1..T}."* This is interpretable and differentiable.

### Example
Scores for token "cat" attending to ["The", "dog", "cat", "chased"]:
```
Scores:  [ -1.0,  -3.0,  -5.0,   1.0 ]
Exp:    [  0.37,   0.05,   0.01,   2.72 ]
Softmax:[  0.26,   0.03,   0.01,   0.70 ]
```
"cat" looks mostly at "chased" (action verb) and a little at itself (identity). The other tokens are mostly ignored.

---

## 8. Embedding Lookup + Positional Encoding

### What
Token IDs are mapped to vectors `E`, and positional encodings `P` are added.

```python
emb = E[token_ids]       # [B, T, d_model]
emb = emb + P[:T, :]     # [B, T, d_model]
```

### Why we do it
With early addition, position and identity are *linearly combined*. The adjacency between "cat" at position 2 and "chased" at position 4 is computed as:
```
(E["cat"] + P_2) - (E["chased"] + P_4)
```
This difference is a simple linear transform away from `(E["cat"] - E["chased"]) + (P_2 - P_4)`.

Because `sinusoidal` encodings are designed so that `P_a - P_b` depends only on `a - b` (relative position), the network can learn to attend to "±2" and "±3" offsets using one linear head, instead of memorizing absolute positions.

### Why it matters
If you used learned positional embeddings (like the original Transformer), the model has to memorize absolute positions. With sinusoidal, the model *generalizes*: it can attend to "the second-to-last word" even if it has never seen a 50-word sentence before.

### Example
"cat" (pos 2), "chased" (pos 4).
Relative offset: +2.

The model can learn a query pattern like:
```
query @ (key at offset +2)  ≈ high
```
This pattern works for any sentence, any length, because offset = +2 is the same pattern computationally wherever it appears.

---

## 9. Two Separations: Why Not One Big Attention?

### What
We separate `W_q`, `W_k`, `W_v`, and `W_out`. Four matrices, not two.

### Why we do it
If we used the same matrix for keys and queries, the query would be constrained to the same subspace as the key. This means:
- The "meaning" of a token (its key) and the "role" it looks for (its query) come from the same 64-dimensional subspace.
- If the model needs to do syntax *and* entity-type relations, it must mix them in every token.

By using different matrices:
- `W_q` projects a token into "what I am looking for" space.
- `W_k` projects into "what I am willing to match against" space.
- `W_v` projects into "what I will broadcast when matched" space.
- `W_out` projects the context-weighted sum back to the model dimension.

This is the most literlly "think" aspect of attention: the query, key, and value are three distinct roles.

### Why it matters
Empirically, sharing `W_q` and `W_k` (or all three) degrades performance. The quarterly-trained models in the literature all use separate projections.

---

## Summary Cheat Sheet

| Operation | What | Why |
|-----------|------|-----|
| **Sinusoidal Pos** | `sin(pos / 10000^{2i/d})` | Inject order without cycles; enables generalization to longer sequences |
| **Scale by `sqrt(d_k)`** | `score / sqrt(d_k)` | Prevent softmax saturation at high dimensions |
| **Multi-head** | Split into `n` groups of size `d_k` | Separate relationship subspaces; capture syntax, semantics, etc. in parallel |
| **LayerNorm** | Normalize per-token per-layer | Keep activations stable across depth; enable gradient flow |
| **Residual** | `x + block(x)` | Allow identity mappings; fix vanishing gradients in deep nets |
| **FFN** | `x @ W1 → ReLU → @ W2` | Non-linearity and dimension expansion; "private" token processing |
| **Softmax** | `exp(score) / sum` | Interpretable probability distribution; fixed budget of attention |
| **Separate Q/K/V/O** | Four different matrices | Uncouple "what I look for", "what matches", "what I say" |

---

## How to Invent Something Similar

If you wanted to design your own Transformer-like architecture from scratch, here is the recipe that the math actually tells you:

1. **Need position?** Don't use learned embeddings (unless you know your max length). Use sinusoidal or learned *relative* offsets.
2. **Need many relationships?** Use multi-head. Start with 4 or 8 heads and `d_model = 64` or `128`.
3. **Training unstable?** Add LayerNorm and residuals.
4. **Deep?** Use residuals + LayerNorm, plus the `sqrt(d_k)` scale.

That is the minimum viable Transformer. Everything else (attention bias, rotary embeddings, multi-query attention) are refinements that solve problems the basic version does not.
