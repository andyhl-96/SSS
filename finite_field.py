# currently this will only generate finite fields of the form Z/pZ
# in the future other finite fields can be considered

import math
import random
from decimal import Decimal, getcontext

class Ffield:
    def __init__(self, p: int) -> None:
        # if p is 0, treat the field as integers
        if p == 0:
            self.order = 0
            self.elems = set([])
            return
        self.elems = set([])
        # get the next (or same) largest prime
        n = p
        is_prime = False
        while not is_prime:
            is_prime = True
            for i in range(2, int(math.sqrt(n)) + 1):
                if n % i == 0:
                    is_prime = False
                    break
            if not is_prime:
                n += 1
        for i in range(n):
            self.elems.add(i)
        self.order = n
    
    def get_class(self, n):
        if self.order == 0:
            return n
        return n % self.order
    def add(self, a, b):
        if self.order == 0:
            return a + b
        return (a + b) % self.order
    def mult(self, a, b):
        if self.order == 0:
            return a * b
        return (a * b) % self.order
    def pow(self, x, y):
        temp = 1
        for i in range(0, y):
            temp *= x
        if self.order == 0:
            return temp
        return temp % self.order
    
    def print_field(self):
        print("Field elements: " + str(self.elems))
        print("Field order: " + str(self.order))

# represents an n degree polynomial in F[x] as a vector of coefficients
class Polynomial:
    def __init__(self, secret, deg, ffield: Ffield) -> None:
        self.coeff = [secret]
        self.field = ffield
        self.shares = []
        self.deg = deg
        for i in range(deg):
            if ffield.order == 0:
                c = random.randint(0, 1000)
                self.coeff.append(c)
            else:
                c = random.randint(0, ffield.order - 1)
                self.coeff.append(c)
    
    # generate k points using the polynomial
    def generate_shares(self, k):
        x_vals = []
        self.shares = []
        for i in range(k):
            y = 0
            if self.field.order == 0:
                x = random.randint(1, 2 * self.deg)
            else:
                x = random.randint(1, self.field.order - 1)
            while x in x_vals:
                if self.field.order == 0:
                    x = random.randint(1, 2 * self.deg)
                else:
                    x = random.randint(1, self.field.order - 1)
            for j in range(len(self.coeff)):
                if self.field.order == 0:
                    y += (self.coeff[j] * self.field.pow(x, j))
                else:
                    y += (self.coeff[j] * self.field.pow(x, j)) % self.field.order
            self.shares.append((x, y))
            x_vals.append(x)
    def print_shares(self):
        print(self.shares)
        pass
    def print_poly(self):
        print(self.coeff)
    def compute_lagrange_constant(self, share, shares):
        getcontext().prec = 1000
        others = []
        for s in shares:
            if s != share:
                others.append(s)
        c = Decimal(1)
        denom = Decimal(1)
        for s in others:
            c *= Decimal(-s[0])
            denom *= (share[0] - s[0])
        return Decimal((c * share[1]) / denom)
    def compute_secret(self, shares: list):
        if len(shares) < self.deg + 1:
            print("Insufficient number of shares")
            return
        c = 0
        for s in shares:
            # compute lagrange
            c += Decimal(self.compute_lagrange_constant(s, shares))
        c = int(c + Decimal(0.5))
        return c


field = Ffield(0)
poly = Polynomial(69, 100, field)
poly.generate_shares(101)
poly.print_shares()
poly.print_poly()

c = poly.compute_secret(poly.shares)
print(str(c))