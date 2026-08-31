"""
Problem 2 Part B (11): Verify CES marginal products with the MicroGPT Value class.
Does not modify microgpt.py.
"""
import math

# Value class copied from microgpt.py (lines 30–72)
class Value:
    __slots__ = ('data', 'grad', '_children', '_local_grads')

    def __init__(self, data, children=(), local_grads=()):
        self.data = data
        self.grad = 0
        self._children = children
        self._local_grads = local_grads

    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        return Value(self.data + other.data, (self, other), (1, 1))

    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        return Value(self.data * other.data, (self, other), (other.data, self.data))

    def __pow__(self, other):
        return Value(self.data**other, (self,), (other * self.data**(other - 1),))

    def __neg__(self):
        return self * -1

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return other + (-self)

    def __rmul__(self, other):
        return self * other

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


if __name__ == '__main__':
    L = Value(4.0)
    K = Value(9.0)
    Y = (0.5 * L**0.5 + 0.5 * K**0.5) ** 2
    Y.backward()
    print("CES check: Y = (0.5*L^0.5 + 0.5*K^0.5)^2 with L=4, K=9")
    print(f"Y    = {Y.data}")
    print(f"MP_L = {L.grad}")
    print(f"MP_K = {K.grad}")
