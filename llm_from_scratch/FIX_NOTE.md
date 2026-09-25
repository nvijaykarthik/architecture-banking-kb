# One-Line Fixes for the transformer to run

I keep running into a NumPy indexing mismatch because `targets` is a 1D array of `numpy.int64: class 'numpy.int64'>` and when I index with `np.arange(B, dtype=np.int64)`, NumPy interprets the result as a NumPy array and tries to use it to index the last axis, causing shape mismatch.

The robust fix is to always scalar-index for single-sample or use Python `int()` cast:

```python
def cross_entropy_loss(logits, targets):
    probs = softmax(logits, axis=-1)
    B = targets.shape[0]
    if B == 1:
        y = int(targets[0])
        return -np.log(float(probs[y, 0]) + 1e-10)
    else:
        # unwrap 1D scalar to Python int to avoid numpy.int64 indexing issues
        idx = np.arange(B, dtype=np.int64)
        return -np.mean(np.log(probs[idx, [int(t) for t in targets]] + 1e-10))
```

But actually, `targets` is already a 1D array `[1]`, not a scalar.

Even simpler robust approach:

```python
def cross_entropy_loss(logits, targets):
    probs = softmax(logits, axis=-1)
    idx = np.arange(len(targets), dtype=np.int64)
    return -np.mean(np.log(probs[idx, targets] + 1e-10))
```

Wait, `targets` is 1D `[1]`, and `idx` will be `[0]`, so `probs[[0], [1]]` still fails if shape mismatch.

The real issue: `targets` is `[1]` (1 element), but we need 3 elements match.

Actually looking at the code: `y = np.array(chunk[1:], dtype=np.int64)` - for a chunk of length 50, this is `[1,2,...,49]` shape `(49,)`.

`logits` is `z @ W_logits + b_logits` which is `[1, 49, vocab_size]`.

`probs` is `[1, 49, vocab_size]`.

`idx = [0, 1, ..., 48]` shape `(49,)`.

`idx, targets` would be `[0, 0, 1, 2]` vs `[1]` (4 items).

We need:
```python
idx = np.arange(logits.shape[1])
log_prob = np.log(probs[0, idx, targets])
```

This is clean and correct.

This is a bug I need to fix in `tiny_transformer.py` and also in `mlp.py`'s `_backprop` if it has the same issue.
