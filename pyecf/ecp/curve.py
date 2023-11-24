import numpy as np
from gmpy2 import f_mod, mpz_random, random_state

from .point import EllipticPoint


class EllipticCurve:
    def __init__(self, n):
        """
        Класс для создания и работы с эллиптическими кривыми
        Parameters
        ----------
        n : Union[int, gmpy2.mpz]
            Факторизируемое число
        """
        self.n = n

        self.x_point = self.generate_random_number()
        self.y_point = self.generate_random_number()
        self.A = self.generate_random_number()
        self.B = f_mod(self.y_point**2 - self.x_point**3 - self.A * self.x_point, self.n)

        if not self.check_singularity():
            raise Exception

    def __str__(self):
        return f"y^2 = x^2 + {self.A}x + {self.B}"

    def generate_random_number(self):
        """
        Функция создает случайное число, равномерно распределенное на интервале [0, 2<<r-1]
        Returns
        -------
        gmpy2.mpz
            Случайное число
        """
        r_state = random_state()
        r = np.random.randint(40, 100)
        return f_mod(mpz_random(r_state, 2 << r).bit_set(0).bit_set(r), self.n)

    def check_singularity(self):
        """
        Проверяет сингулярность созданной кривой
        Returns
        -------
        bool
            Является ли кривая сингулярной
        """
        return f_mod(4 * (self.A * self.A * self.A) + 27 * (self.B * self.B), self.n) != 0

    def random_point(self):
        """
        # DEPRECATED
        Создание случайной точки на кривой
        Returns
        -------
        EllipticPoint
            Случайная точка на кривой
        """
        return EllipticPoint(self.x_point, self.y_point, self)

    def check_point_belonging(self, point):
        """
        Проверяет, принадлежит ли выбранная точка кривой
        Parameters
        ----------
        point : EllipticPoint
            Точка

        Returns
        -------
        bool
            Принадлежит ли точка кривой
        """
        return f_mod(point.y**2, self.n) == f_mod(point.x**3 + self.A * point.x + self.B, self.n)
