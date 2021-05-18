import sage.all
from sage.sets.primes import Primes

import sys
import time
from gmpy2 import mpz, f_mod
import numpy as np

from utils.misc import full_power
from ECP import EllipticCurve, EllipticPoint, is_point
from logger import logger

log = logger.get_logger(__name__)


class LenstraAlgorithm:
    def __init__(self, n):
        """
        Основной класс алгоритма факторизации числа с помощью алгоритма Ленстры
        Последовательно проходится по делителям числа <n>, проверяя на простоту. Если число составное, запускается
        алгоритм поиска делителя. Массив делителей пополняется новым числом и числом на предыдущей итерации, деленное
        на найденный делитель. Число с прошлой итерации удаляется.

        Использование:

        # >>>   n = int(...) -- любое целое число > 1
        # >>>   lenstra_algo = LenstraAlgorithm(n)
        # >>>   factors = lenstra_algo.factorize()

        Parameters
        ----------
        n : Union[int, gmpy2.mpz]
            Число, которое необходимо разложить (рекомендуется использовать числа в 20-25 знаков или 64-83 бита)
        """
        self.n = n

        self.not_prime_factors = [n]
        self.prime_factors = list()

        self.pre_primes = Primes()

    def check_prime(self, n):
        """
        Функция проверки простоты числа (используется класс Primes из библиотеки sage)
        Parameters
        ----------
        n : Union[int, gmpy2.mpz]
            Число для проверки
        Returns
        -------
        bool
            Простое ли число
        """
        if n in self.pre_primes:
            return True
        else:
            return False

    @staticmethod
    def generate_random_curve(n, retries=10):
        """
        Функция генерирования случайной эллиптической кривой
        Parameters
        ----------
        n : Union[int, gmpy2.mpz]
            Факторизируемое число
        retries : int
            Количество повторений генерирования кривой

        Returns
        -------
        EllipticCurve
            Сгенерированная кривая (в случае удачи на 10 итерациях)
        """
        for i in range(retries):
            try:
                random_curve = EllipticCurve(n)
                return random_curve
            except:
                continue
        log.error(f"После 10 попыток не удалось сгенерировать кривую, перезапустите модуль")
        sys.exit(1)

    def find_factor(self, n):
        """
        Алгоритм Ленстры
        Parameters
        ----------
        n : Union[int, gmpy2.mpz]
            Факторизируемое число
        Returns
        -------
        gmp2.mpz
            Делитель или 1
        """
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
        """
        Один раунд факторизации:
         - проверяется простота числа
         - проверяется делимость на 2 и 3
         - если два предыдущих этапа не выполняются, то запускается алгоритм Ленстры

        Parameters
        ----------
        n : Union[int, gmpy2.mpz]
            Факторизируемое число
        """
        if self.check_prime(n):
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
        """
        Обертка факторизации для выделения текущего числа для факторизации
        Returns
        -------
        numpy.ndarray
            Отсортированный список простых делителей
        """
        start_time = time.time()
        while len(self.not_prime_factors):
            current_factor = self.not_prime_factors[0]
            self.one_round_factorization(current_factor)
            self.not_prime_factors.pop(0)
        end_time = time.time() - start_time
        log.info(f"Факторизация выполнилась за {end_time} сек")
        return np.sort(self.prime_factors)

    def check_factorization(self, factors):
        """
        Проверяет, верно ли было разложено число перемножением всех делителей
        Parameters
        ----------
        factors : Union[numpy.ndarray, list]
            Делители
        Returns
        -------
        bool
            Верно ли разложено число
        """
        return self.n == np.prod(list(map(int, factors)))
