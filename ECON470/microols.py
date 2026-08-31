"""
Using the optimization machinery in microgpt.py to train and run least squares inference. This file is OLS solved by gradient descent and backpropagation --- total overkill for OLS, but it shows that the principles are the same.

Adapted from microgpt.py by @karpathy
"""

import os       # os.path.exists
import csv      # csv.DictReader
import math     # math.log, math.exp, math.sqrt
import random   # random.seed, random.choices, random.gauss, random.shuffle
random.seed(42) # Let there be order among chaos

# Let there be a Dataset: orange juice prices, sales, and brands from supermarket scanners
if not os.path.exists('oj.csv'):
    import urllib.request
    oj_url = 'https://raw.githubusercontent.com/eduardo-zambrano/BDS/master/examples/oj.csv'
    urllib.request.urlretrieve(oj_url, 'oj.csv')
docs = []
with open('oj.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        s, p = float(row['sales']), float(row['price'])
        brand = row['brand']
        if s > 0 and p > 0:
            mm = 1.0 if brand == 'minute.maid' else 0.0
            tr = 1.0 if brand == 'tropicana' else 0.0
            docs.append((math.log(p), mm, tr, math.log(s)))
random.shuffle(docs)
print(f"num observations: {len(docs)}")

# Let there be Autograd to recursively apply the chain rule through a computation graph
class Value:
    __slots__ = ('data', 'grad', '_children', '_local_grads')

    def __init__(self, data, children=(), local_grads=()):
        self.data = data                # scalar value of this node calculated during forward pass
        self.grad = 0                   # derivative of the loss w.r.t. this node, calculated in backward pass
        self._children = children       # children of this node in the computation graph
        self._local_grads = local_grads # local derivative of this node w.r.t. its children

    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        return Value(self.data + other.data, (self, other), (1, 1))

    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        return Value(self.data * other.data, (self, other), (other.data, self.data))

    def __pow__(self, other): return Value(self.data**other, (self,), (other * self.data**(other-1),))
    def __neg__(self): return self * -1
    def __radd__(self, other): return self + other
    def __sub__(self, other): return self + (-other)
    def __rsub__(self, other): return other + (-self)
    def __rmul__(self, other): return self * other
    def __truediv__(self, other): return self * other**-1
    def __rtruediv__(self, other): return other * self**-1

    def backward(self):
        topo = []
        visited = set()
        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v._children:
                    build_topo(child)
                topo.append(v)
        build_topo(self)
        self.grad = 1
        for v in reversed(topo):
            for child, local_grad in zip(v._children, v._local_grads):
                child.grad += local_grad * v.grad

# Initialize the parameters, to store the knowledge of the model
a    = Value(0.0)  # slope on ln(price): the demand elasticity
b_mm = Value(0.0)  # brand dummy: minute maid (relative to dominicks)
b_tr = Value(0.0)  # brand dummy: tropicana (relative to dominicks)
b0   = Value(0.0)  # intercept
params = [a, b_mm, b_tr, b0]
print(f"num params: {len(params)}")

# Let there be a Forward Pass: the model's prediction for a single observation
def predict(lnp, mm, tr):
    return a * lnp + b_mm * mm + b_tr * tr + b0  # ln(Q) = a*ln(P) + b_mm*MM + b_tr*TR + b0

# Let there be Training to learn the parameters via gradient descent
num_steps = 10000
batch_size = 32  # mini-batch: average over this many observations per step
lr = 0.01        # learning rate
beta1, beta2, eps_adam = 0.9, 0.999, 1e-8 # Adam optimizer hyperparameters
m = [0.0] * len(params)
v = [0.0] * len(params)

print(f"training for {num_steps} steps...")
for step in range(num_steps):

    # Sample a mini-batch of observations
    batch = random.choices(docs, k=batch_size)

    # Forward the batch through the model, building up the computation graph all the way to the loss
    total_loss = Value(0.0)
    for lnp, mm, tr, lns in batch:
        y_hat = predict(lnp, mm, tr)
        total_loss = total_loss + (y_hat - lns) ** 2
    loss = total_loss * (1.0 / batch_size) # average squared error. May yours be low.

    # Backward the loss, calculating the gradients with respect to all model parameters
    loss.backward()

    # Adam optimizer step: update the parameters using the gradients
    for i, p in enumerate(params):
        m[i] = beta1 * m[i] + (1 - beta1) * p.grad
        v[i] = beta2 * v[i] + (1 - beta2) * p.grad ** 2
        m_hat = m[i] / (1 - beta1 ** (step + 1))
        v_hat = v[i] / (1 - beta2 ** (step + 1))
        p.data -= lr * m_hat / (v_hat ** 0.5 + eps_adam)
        p.grad = 0

    print(f"step {step+1:5d} / {num_steps} | loss {loss.data:.4f} | a = {a.data:.4f}  b0 = {b0.data:.4f}  b_mm = {b_mm.data:.4f}  b_tr = {b_tr.data:.4f}", end='\r')

# Compute the residual standard error (for sampling)
ssr = sum((lns - (a.data * lnp + b_mm.data * mm + b_tr.data * tr + b0.data))**2 for lnp, mm, tr, lns in docs)
se = math.sqrt(ssr / (len(docs) - len(params)))

print(f"\n\n--- trained model ---")
print(f"ln(Q) = {a.data:.4f} * ln(P) + {b_mm.data:.4f} * MinuteMaid + {b_tr.data:.4f} * Tropicana + {b0.data:.4f}")
print(f"demand elasticity: {a.data:.4f}")
print(f"residual standard error: {se:.4f}")

# Inference: sample from the conditional distribution Q | P = $3.00, brand = Tropicana
price = 3.00
x_lnp = math.log(price)
x_mm, x_tr = 0.0, 1.0  # Tropicana
y_hat = a.data * x_lnp + b_mm.data * x_mm + b_tr.data * x_tr + b0.data
print(f"\n--- inference: 20 draws from Q | P = ${price:.2f}, brand = Tropicana ---")
print(f"predicted ln(Q) = {y_hat:.4f}")
print()
for i in range(20):
    ln_q = y_hat + random.gauss(0, se)
    q = math.exp(ln_q)
    print(f"sample {i+1:2d}: Q = {q:,.0f} units")
