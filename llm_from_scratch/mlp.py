import numpy as np


class Activation:
    relu = lambda x: np.maximum(0, x)


class MLP:
    def __init__(self, layer_sizes, activation="relu"):
        self.layer_sizes = layer_sizes
        self.activation = getattr(Activation, activation, Activation.relu)
        self.weights = [
            np.random.randn(in_dim, out_dim)
            .astype(np.float32)
            * np.sqrt(2.0 / in_dim)
            for in_dim, out_dim in zip(layer_sizes[:-1], layer_sizes[1:])
        ]
        self.biases = [
            np.zeros(out_dim, dtype=np.float32)
            for out_dim in layer_sizes[1:]
        ]
        self.cache = [None] * (len(layer_sizes) - 1)

    def forward(self, x):
        a = x.reshape(x.shape[0], -1)
        for i, (W, b) in enumerate(zip(self.weights, self.biases)):
            z = a @ W + b
            self.cache[i] = (a, W, b, z)
            a = Activation.relu(z) if i < len(self.weights) - 1 else z
        return a

    def backward(self, x, y, lr=1e-3):
        target = np.zeros_like(self.cache[-1][3])
        target[0, int(y)] = 1.0
        loss_grad = self.cache[-1][3] - target
        _backprop(self, loss_grad, lr=lr)

    def save(self, path):
        np.savez(
            path,
            weights=np.array(self.weights, dtype=object),
            biases=np.array(self.biases, dtype=object),
            layer_sizes=np.array(self.layer_sizes, dtype=np.int32),
        )

    @classmethod
    def load(cls, path):
        data = np.load(path)
        instance = object.__new__(cls)
        instance.layer_sizes = data["layer_sizes"].tolist()
        instance.weights = [
            data["weights"][i] for i in range(data["weights"].shape[0])
        ]
        instance.biases = [
            data["biases"][i] for i in range(data["biases"].shape[0])
        ]
        return instance


def _backprop(model, g_z=None, lr=1e-3):
    if g_z is None:
        raise ValueError("need g_z")
    for i in reversed(range(len(model.cache))):
        a_prev, W, b, z = model.cache[i]
        g = g_z if i == len(model.weights) - 1 else g_z * (z > 0)
        dW = a_prev.T @ g
        db = np.sum(g, axis=0)
        g_z = g @ W.T
        model.weights[i] -= lr * dW
        model.biases[i] -= lr * db
    model.cache = [None] * len(model.weights)


def train(
    model,
    X_train,
    Y_train,
    epochs=200,
    batch_size=32,
    lr=1e-3,
    verbose=100,
):
    Y_train = np.asarray(Y_train).reshape(-1).astype(np.int64)
    n = X_train.shape[0]
    for epoch in range(1, epochs + 1):
        idx = np.random.permutation(n)
        X_shuf = X_train[idx]
        Y_shuf = Y_train[idx]
        for start in range(0, n, batch_size):
            xb = X_shuf[start : start + batch_size]
            yb = Y_shuf[start : start + batch_size]
            a = xb.reshape(xb.shape[0], -1)
            for i, (W, b) in enumerate(zip(model.weights, model.biases)):
                z = a @ W + b
                model.cache[i] = (a, W, b, z)
                a = Activation.relu(z) if i < len(model.weights) - 1 else z
            target = np.zeros(model.cache[-1][3].shape, dtype=np.float32)
            target[np.arange(len(yb)), yb] = 1.0
            diff = model.cache[-1][3] - target
            _backprop(model, diff, lr=lr)
        if verbose and epoch % verbose == 0:
            loss = 0.0
            pred = np.empty(n, dtype=np.int64)
            for j, (xi, yi) in enumerate(zip(X_train, Y_train)):
                out = model.forward(xi.reshape(1, -1))
                loss += float(np.sum(out**2) / xi.shape[0])
                pred[j] = int(np.argmax(out))
            acc = np.mean(pred == Y_train)
            print(f"epoch {epoch} loss {loss:.4f} acc {acc:.4f}")


if __name__ == "__main__":
    X_train = np.loadtxt("X.txt", dtype=np.float32, comments="#")
    Y_train = np.loadtxt("Y.txt", dtype=np.float32, comments="#")
    model = MLP(
        layer_sizes=[X_train.shape[1], 32, 16, 2],
        activation="relu",
    )
    train(model, X_train, Y_train, epochs=300, batch_size=16, lr=0.05, verbose=20)
    xi = np.array([[0.1, 3.2, 4.5, 1.3]], dtype=np.float32)
    print(model.forward(xi))
    print(int(np.argmax(model.forward(xi))))
    xi2 = np.array([[2.0, 0.1, 0.1, 0.1]], dtype=np.float32)
    print(model.forward(xi2))
    print(int(np.argmax(model.forward(xi2))))
    model.save("model.npz")
    print("saved model.npz")
