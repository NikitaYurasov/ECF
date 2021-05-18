import sys
from gmpy2 import mpz, f_mod
import numpy as np

from utils.misc import full_power
from ECP import EllipticCurve, EllipticPoint, is_point

prime = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107,
         109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
         233, 239, 241, 251, 257, 263, 269, 271]


class LenstraAlgorithm:
    def __init__(self, n):
        self.n = n

        self.not_prime_factors = [n]
        self.prime_factors = list()

    @staticmethod
    def check_prime(n):
        pass

    @staticmethod
    def generate_random_curve(n):
        for i in range(10):
            try:
                random_curve = EllipticCurve(n)
                return random_curve
            except:
                continue
        sys.exit(1)

    def find_factor(self, n):
        random_curve = self.generate_random_curve(n)
        random_point = EllipticPoint(random_curve.x_point, random_curve.y_point, curve=random_curve)
        k = np.random.randint(100000, 500000)
        i = 2
        while i < k:
            i += 1
            random_point = random_point ** i
            if not is_point(random_point):
                return random_point
        return mpz(1)

    def one_round_factorization(self, n):
        if n in prime:
            self.prime_factors.append(mpz(n))
        else:
            best_power, best_base = full_power(n)
            if best_power != 1:
                for i in range(best_power):
                    self.not_prime_factors.append(best_base)
            elif f_mod(n, 2) == 0:
                self.prime_factors.append(mpz(2))
                self.not_prime_factors.append(mpz(n // 2))
            elif f_mod(n, 3) == 0:
                self.prime_factors.append(mpz(3))
                self.not_prime_factors.append(mpz(n // 3))
            else:
                divider = self.find_factor(n)
                self.not_prime_factors.append(divider)
                self.not_prime_factors.append(n // divider)

    def factorize(self):
        while len(self.not_prime_factors):
            current_factor = self.not_prime_factors[0]
            self.one_round_factorization(current_factor)
            self.not_prime_factors.pop(0)
        return np.sort(self.prime_factors)

    def check_factorization(self, factors):
        return self.n == np.prod(list(map(int, factors)))


if __name__ == '__main__':
    n = 11 * 15 * 17 * 21 * 255 * 513 * 99 * 127 * 133
    print(f"Factorizing n = {n}")
    n = mpz(n)
    algo = LenstraAlgorithm(n)
    factors = algo.factorize()
    if algo.check_factorization(factors):
        print(f"{n} = {'*'.join(list(map(str, factors)))}")
