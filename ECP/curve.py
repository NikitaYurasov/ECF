import numpy as np
from gmpy2 import random_state, mpz_random, f_mod

from .point import EllipticPoint


class EllipticCurve:
    def __init__(self, n, seed=None):
        self.n = n

        self.x_point = self.generate_random_number(seed=seed)
        self.y_point = self.generate_random_number(seed=seed)
        self.A = self.generate_random_number(seed=seed)
        self.B = f_mod(self.y_point ** 2 - self.x_point ** 3 - self.A * self.x_point, self.n)

        if not self.check_singularity():
            raise Exception

    def generate_random_number(self, seed=None):
        r_state = random_state()
        r = np.random.randint(40, 100)
        return f_mod(mpz_random(r_state, 2 << r).bit_set(0).bit_set(r), self.n)

    def check_singularity(self):
        return f_mod(4 * (self.A * self.A * self.A) + 27 * (self.B * self.B), self.n) != 0

    def random_point(self):
        return EllipticPoint(self.x_point, self.y_point, self)

    def check_point_belonging(self, point):
        return f_mod(point.y ** 2, self.n) == f_mod(point.x ** 3 + self.A * point.x + self.B, self.n)
