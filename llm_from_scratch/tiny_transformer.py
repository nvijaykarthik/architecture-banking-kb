"""
Tiny transformer written in pure Python + NumPy.

No PyTorch, no TensorFlow, no external packages.
"""
import random
import numpy as np


def build_vocab(text):
    tokens = text.lower().replace("\n", " ").split(" ")
    vocab = {"<pad>": 0, "<unk>": 1}
    for t in tokens:
        if t not in vocab:
            vocab[t] = len(vocab)
    rev = {i: t for t, i in vocab.items()}
    return vocab, rev


def matmul_bmm(a, b):
    return a @ b


def softmax(z, axis=-1):
    m = np.max(z, axis=axis, keepdims=True)
    return np.exp(z - m) / np.sum(np.exp(z - m), axis=axis, keepdims=True)


class FFNN:
    def __init__(self, in_dim, hidden_dim, out_dim, activation="relu"):
        self.W1 = np.random.randn(in_dim, hidden_dim) * np.sqrt(2.0 / in_dim)
        self.b1 = np.zeros(hidden_dim)
        self.W2 = np.random.randn(hidden_dim, out_dim) * np.sqrt(2.0 / hidden_dim)
        self.b2 = np.zeros(out_dim)
        self.activation = activation

    def forward(self, x):
        self.cache = {"a": None, "z1": None, "a1": None, "z2": None}
        a = x
        self.cache["a"] = a
        z1 = matmul_bmm(a, self.W1) + self.b1
        self.cache["z1"] = z1
        a1 = z1
        a1[z1 < 0] = 0
        self.cache["a1"] = a1
        z2 = matmul_bmm(a1, self.W2) + self.b2
        self.cache["z2"] = z2
        return z2

    def backward(self, grad, lr=1e-3):
        z1 = self.cache["z1"]
        a1 = self.cache["a1"]
        dW2 = a1.T @ grad
        db2 = np.sum(grad, axis=0)
        d_hidden = grad @ self.W2.T
        da1 = np.multiply(d_hidden, (z1 > 0))
        dW1 = self.cache["a"].T @ da1
        db1 = np.sum(da1, axis=0)
        self.W2 -= lr * dW2
        self.b2 -= lr * db2
        self.W1 -= lr * dW1
        self.b1 -= lr * db1


class MultiHeadAttention:
    def __init__(self, d_model, n_heads, lr=1e-3):
        self.d_model = d_model
        self.n_heads = n_heads
        self.d_k = d_model // n_heads
        self.W_q = np.random.randn(d_model, d_model) * np.sqrt(2.0 / d_model)
        self.W_k = np.random.randn(d_model, d_model) * np.sqrt(2.0 / d_model)
        self.W_v = np.random.randn(d_model, d_model) * np.sqrt(2.0 / d_model)
        self.W_out = np.random.randn(d_model, d_model) * np.sqrt(2.0 / d_model)
        self.b_out = np.zeros(d_model)
        self.lr = lr
        self.cache = []

    def forward(self, x):
        B, T, C = x.shape
        q = matmul_bmm(x, self.W_q)
        k = matmul_bmm(x, self.W_k)
        v = matmul_bmm(x, self.W_v)

        q = q.reshape(B, T, self.n_heads, self.d_k)
        k = k.reshape(B, T, self.n_heads, self.d_k)
        v = v.reshape(B, T, self.n_heads, self.d_k)

        scale = 1.0 / np.sqrt(self.d_k)
        raw = matmul_bmm(q, k.transpose(0, 1, 3, 2))
        raw = raw * scale
        scores = softmax(raw, axis=-1)
        attn = matmul_bmm(scores, v)
        attn = attn.reshape(B, T, self.d_model)
        out = matmul_bmm(attn, self.W_out) + self.b_out
        self.cache = [x, q, k, v, scores, v, out]
        return out

    def backward(self, grad, lr=None):
        if lr is None:
            lr = self.lr
        x, q, k, v, scores, v_head, out = self.cache
        B, T, _ = out.shape
        self.W_out -= lr * matmul_bmm(grad, v.transpose(0, 1, 3, 2)).reshape(self.d_model, self.d_model)
        dv = matmul_bmm(
            scores.transpose(0, 1, 2, 3),
            grad.reshape(B, T, self.n_heads, self.d_k),
        ).reshape(B, T, self.d_model)
        K_transposed = v.transpose(0, 1, 3, 2).reshape(B, T, self.n_heads, self.d_k)
        K_transposed = K_transposed.transpose(0, 1, 2, 3)
        D = (
            matmul_bmm(
                K_transposed,
                dv.reshape(B, T, self.n_heads, self.d_k),
            )
            .transpose(0, 1, 2, 3)
            / T
        )
        self.W_v -= lr * D
        dscores = matmul_bmm(grad, self.W_out.T)
        dscores = dscores.reshape(B, T, self.n_heads, self.d_k)
        dq = dscores @ k.reshape(B, T, self.n_heads, self.d_k)
        return dq.transpose(0, 1, 2, 3).reshape(B, T, self.d_model)


def sinpos(pos, d, m):
    return np.sin(pos / (10000 ** (2 * np.arange(d) / m)))


def build_positional_encoding(seq_len, d_model):
    pe = np.zeros((seq_len, d_model))
    for t in range(seq_len):
        pe[t] = sinpos(t, d_model, d_model)
    return pe


def cross_entropy_loss(logits, targets):
    probs = softmax(logits, axis=-1)
    idx = np.arange(logits.shape[1], dtype=np.int64)
    return -np.mean(np.log(probs[0, idx, (targets).astype(np.int64)] + 1e-10))


def main():
    np.random.seed(0)
    random.seed(0)
    corpus = (
        "the quick brown fox jumps over the lazy dog " * 8
    )
    vocab, rev = build_vocab(corpus)
    toks = corpus.lower().replace("\n", " ").split(" ")
    ids = [vocab.get(t, 1) for t in toks]
    E = 8
    nh = 2
    vocab_size = len(vocab)
    M = np.random.randn(vocab_size, E) * np.sqrt(2.0 / E)
    pe = build_positional_encoding(500, E)
    ffn = FFNN(E, 2 * E, E, activation="relu")
    W_logits = np.random.randn(E, vocab_size) * np.sqrt(2.0 / E)
    b_logits = np.zeros(vocab_size)

    seq_len = 50
    for epoch in range(1, 26):
        loss = 0.0
        count = 0
        for i in range(0, len(ids) - seq_len, seq_len):
            chunk = ids[i:i + seq_len]
            X = np.array(chunk[:-1], dtype=np.int64).reshape(1, -1)
            y = np.array(chunk[1:], dtype=np.int64)
            emb = M[X, :] + pe[:X.shape[1], :]
            z = ffn.forward(emb)
            logits = z @ W_logits + b_logits
            loss += cross_entropy_loss(logits, y)
            count += 1
            dlogits = softmax(logits)
            idx = np.arange(y.shape[0])
            y_int = y.astype(np.int64).ravel()
            dlogits[idx.tolist(), y_int] -= 1
            d_ffn = dlogits @ W_logits
            ffn.backward(d_ffn, lr=1e-3)
        print(f"epoch {epoch} loss {loss/count:.4f}")

    prompt = "the quick"
    inp = np.array([vocab.get(t, 1) for t in prompt.split()], dtype=np.int64).reshape(1, -1)
    for _ in range(10):
        emb = M[inp, :] + pe[prompt.count(" "):, :]
        z = ffn.forward(emb)
        logits = z @ W_logits + b_logits
        probs = softmax(logits, axis=-1)
        nxt = np.argmax(probs, axis=-1)[0, -1]
        print(rev.get(nxt, "?"), end=" ")
        inp = np.array([[inp[0, -1], int(nxt)]])
    print()


if __name__ == "__main__":
    main()
