"""Create train data and run a small NN."""
import os, numpy as np

def make_X(n0, n1):
    zero = np.array([0.1, 3.2, 4.5, 1.3], dtype=np.float32)
    one = np.array([2.0, 0.1, 0.1, 0.1], dtype=np.float32)
    return np.vstack([np.tile(zero, (n0, 1)), np.tile(one, (n1, 1))])

def make_Y(n0, n1):
    zeros = np.zeros(n0, dtype=np.float32)
    ones = np.ones(n1, dtype=np.float32)
    return np.hstack([zeros, ones])

X = make_X(24, 24)
Y = make_Y(24, 24)
os.makedirs("data", exist_ok=True)
with open("X.txt", "w") as f:
    f.write("\n".join(" ".join(map(str, row)) for row in X) + "\n")
with open("Y.txt", "w") as f:
    f.write("\n".join(map(str, Y)) + "\n")
print("Data written to X.txt / Y.txt", X.shape, Y.shape)

import numpy as np
import mlp

np.random.seed(0)
model = mlp.MLP(layer_sizes=[X.shape[1], 32, 16, 2], activation="relu")
mlp.train(model, X, Y, epochs=300, batch_size=16, lr=0.2, verbose=20)
xi = np.array([[0.1, 3.2, 4.5, 1.3]], dtype=np.float32)
print("class 0 input:", model.forward(xi))
print("each 0:", np.argmax(model.forward(xi)))
xi2 = np.array([[2.0, 0.1, 0.1, 0.1]], dtype=np.float32)
print("class 1 input:", model.forward(xi2))
print("each 1:", np.argmax(model.forward(xi2)))
model.save("model.npz")
print("saved model.npz")
