import numpy as np
np.random.seed(0)
from mlp import MLP, train

zero = np.array([0.1, 3.2, 4.5, 1.3], dtype=np.float32)
one = np.array([2.0, 0.1, 0.1, 0.1], dtype=np.float32)
X = np.vstack([np.tile(zero, (24, 1)), np.tile(one, (24, 1))])
Y = np.hstack([np.zeros(24, dtype=np.float32), np.ones(24, dtype=np.float32)])
with open('X.txt', 'w') as f:
    f.write('\n'.join(' '.join(f'{x}' for x in row) for row in X) + '\n')
with open('Y.txt', 'w') as f:
    f.write('\n'.join(f'{int(y)}' for y in Y) + '\n')
print('Data saved', X.shape, Y.shape)
model = MLP(layer_sizes=[4, 32, 16, 2], activation='relu')
train(model, X, Y, epochs=300, batch_size=16, lr=0.05, verbose=20)
print('class 0', model.forward(np.array([[0.1, 3.2, 4.5, 1.3]], dtype=np.float32)))
print('class 1', model.forward(np.array([[2.0, 0.1, 0.1, 0.1]], dtype=np.float32)))
model.save('model.npz')
print('saved model.npz')
