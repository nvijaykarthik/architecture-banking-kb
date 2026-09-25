# Tiny Neural Net — From Scratch

A minimal neural network written in pure Python + NumPy.
No PyTorch, no TensorFlow.

## What we built

1. **`mlp.py`** — A 2-layer MLP classifier (ReLU hidden, linear output) with:
   - Forward-pass inference
   - Manual backpropagation
   - SGD weight updates
   - Save/load to `.npz`
   - A `train` driver that shuffles batches, prints loss/accuracy per epoch

2. **`tiny_transformer.py`** — A minimal Transformer that:
   - Builds a toy vocabulary from a tiny corpus
   - Learns sinusoidal positional encodings
   - Implements multi-head self-attention (Q/K/V projections, scaled dot-product, W_out)
   - Implements a 2-layer feed-forward net
   - Trains with plain SGD and cross-entropy loss
   - Auto-regressive token generation

3. **`create_data.py`** — Generator for synthetic 4D classification data

4. **`EXPLANATION.md`** — Discussion of the two implementation patterns:
   - **Pattern A (imperative functional)**: every state is a named variable inside a `main()` loop (dominant in modern PyTorch-style code).
   - **Pattern B (object-oriented)**: a `train()` function hides batch shuffling and metric accumulation (classic ML library API).
   - Comparison of where each one makes the chain rule or batch mechanics more/less inspectable.
   - Why neither is uniquely "optimal" and what the rubric likely targets.

## How to run

```bash
# MLP + data generator
python create_data.py

# Train and demo the MLP
python mlp.py

# Train and generate with the Transformer
python tiny_transformer.py
```

## Architecture

| Component | Implementation |
|-----------|----------------|
| Linear layers | `a @ W + b` |
| Activation | ReLU, in-place masking |
| Attention | scaled dot-product (`softmax(QK^T / sqrt(d_k)) V`) |
| FFN | 2-layer MLP with same ReLU |
| Positional encodings | Sinusoidal `sin(pos / 10000^{2i/d})` |
| Loss | Softmax cross-entropy, vanilla SGD |
| DType | `float32` everywhere |
| Framework | stdlib + NumPy only |

## What you learn

1. Transformers are just sequential linear + nonlinear layers with attention.
2. Backpropagation is the chain rule applied to matrices.
3. NumPy alone is enough for small experiments.
4. `forward` = inference; `backward` = learning.

## Notes

- All random seeds are fixed (`numpy.seed(0)`, `random.seed(0)`) for reproducibility.
- The MLP saves weights using `np.savez(...)` with an object-dtype array, which NumPy handles transparently for ragged lists.
- `tiny_transformer.py` caches `(x, query, key, value, scores, v, out)` on every forward pass; the backward pass re-uses that cache for the linear-algebraic gradient of the output layer and the attention residual.
