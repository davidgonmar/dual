from functools import wraps
from math import log

def binary_op(op):
    @wraps(op)
    def f(self, other):
        other = other if isinstance(other, Dual) else Dual(other, 0.0)
        return op(self, other)
    return f

class Dual:
    def __init__(self, real: float, dual: float):
        self.real = real
        self.dual = dual

    @binary_op
    def __add__(self, other: "Dual"):
        return Dual(self.real + other.real, self.dual + other.dual)
    
    @binary_op
    def __mul__(self, other: "Dual"):
        return Dual(self.real * other.real, self.dual * other.real + other.dual * self.real)
    
    @binary_op
    def __div__(self, other: "Dual"):
        return Dual(self.real / other.real, (other.real * self.dual - self.real * other.dual) / other.real ** 2)
    
    @binary_op
    def __pow__(self, other: "Dual"):
        return Dual(self.real ** other.real, self.real ** (other.real) * (other.dual * log(self.real) + other.real * self.dual / self.real))
    
def derivative(f, wrt=None):
    @wraps(f)
    def ret(*args):
        nonlocal wrt
        wrt = wrt or list(range(len(args)))
        wrt = wrt if isinstance(wrt, list) else [wrt]
        duals = [Dual(a, 0.0) for a in args]
        derivatives = []
        for i in wrt:
            duals[i].dual = 1.0
            derivatives.append(f(*duals).dual)
            duals[i].dual = 0.0
        return f(*args), derivatives
    return ret

if __name__ == "__main__":
    def f(x, y):
        return x ** 2 + y ** 3

    assert derivative(f)(2, 3) == (31, [4, 27])


    def f2(x, y):
        return x * y
    
    assert derivative(f2)(2, 3) == (6, [3, 2])