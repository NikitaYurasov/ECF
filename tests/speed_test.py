import time
from tqdm import tqdm
from sympy import prod, sieve, prime
import matplotlib.pyplot as plt
from pyecf import LenstraAlgorithm

n_numbers = 100
x_arr = list(range(2, n_numbers))
y_arr = []
for i in tqdm(range(2, n_numbers)):
    primes = sieve.primerange(2, prime(i) + 1)
    mult = prod(primes)

    algo = LenstraAlgorithm(int(mult), omega=10, nu=prime(i) + 1)
    start_time = time.time()
    factors = algo.factorize()
    end_time = time.time() - start_time
    t = algo.check_factorization(factors)
    y_arr.append(end_time)
plt.figure(figsize=(20, 10))
plt.plot(x_arr, y_arr)
plt.grid()
plt.savefig('./speedtest_run.jpg')
plt.show()
