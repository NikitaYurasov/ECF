from gmpy2 import f_mod, gcd, invert


def is_point(point):
    """
    Функция проверки типа точки (делителя)
    Parameters
    ----------
    point : Union[EllipticPoint, IdentityEllipticPoint, gmpy2.mpz, int]
        Точка, делитель

    Returns
    -------
    bool
        Является ли точка эллиптической точкой или делителем
    """
    return isinstance(point, (EllipticPoint, IdentityEllipticPoint))


class IdentityEllipticPoint:
    def __init__(self, curve):
        """
        Класс нейтральной точки на эллиптической кривой
        Parameters
        ----------
        curve : EllipticCurve
            Эллиптическая кривая
        """
        self.curve = curve

    def __str__(self):
        return f"IdentityEllipticPoint"

    def __add__(self, other):
        """
        Перегрузка оператора сложения
        Parameters
        ----------
        other : Union[EllipticPoint, IdentityEllipticPoint]
            Точка для сложения

        Returns
        -------
        Union[EllipticPoint, IdentityEllipticPoint]
            Другая точка
        """
        if isinstance(other, (EllipticPoint, IdentityEllipticPoint)):
            return other
        else:
            raise AttributeError

    def __pow__(self, power, modulo=None):
        """
        Перегрузка оператора возведения в степень
        Parameters
        ----------
        power : int
            Степень
        modulo : None
            deprecated
        Returns
        -------
        IdentityEllipticPoint
            Возвращает себя же
        """
        return self


class EllipticPoint:
    def __init__(self, x, y, curve):
        """
        Класс точки на эллиптической кривой
        Parameters
        ----------
        x : Union[gmpy2.mpz, int]
            1-я координата точки
        y : Union[gmpy2.mpz, int]
            2-я координата точки
        curve : EllipticCurve
            Эллиптическая кривая
        """
        self.curve = curve
        self.x = x
        self.y = y

        if not self.curve.check_point_belonging(self):
            raise Exception('Point does not belong to the curve')

    def __str__(self):
        return f"({self.x, self.y})"

    def __add__(self, other):
        """
        Перегрузка оператора сложения
        Алгоритм соответствует предложенному Ленстрой (partial addition)
        Parameters
        ----------
        other : Union[EllipticPoint, IdentityEllipticPoint]

        Returns
        -------
        Union[EllipticPoint, IdentityEllipticPoint, gmpy2.mpz]
            Результирующая точка или делитель
        """
        if isinstance(other, EllipticPoint):
            d = gcd(self.x - other.x, self.curve.n)
            if 1 < d < self.curve.n:
                return d
            if d == 1:
                iv = invert(f_mod(self.x - other.x, self.curve.n), self.curve.n)
                s = f_mod((self.y - other.y) * iv, self.curve.n)
                x_res = f_mod(s**2 - self.x - other.x, self.curve.n)
                y_res = f_mod(-self.y - s * (x_res - self.x), self.curve.n)
                return EllipticPoint(x=x_res, y=y_res, curve=self.curve)
            else:
                d = gcd(self.y + other.y, self.curve.n)
                if 1 < d < self.curve.n:
                    return d
                if d == self.curve.n:
                    return IdentityEllipticPoint(self.curve)
                elif d == 1:
                    iv = invert(f_mod(self.y + other.y, self.curve.n), self.curve.n)
                    s = f_mod((3 * self.x * self.x + self.curve.A) * iv, self.curve.n)
                    x_res = f_mod(s * s - self.x - other.x, self.curve.n)
                    y_res = f_mod(-self.y - s * (x_res - self.x), self.curve.n)
                    return EllipticPoint(x=x_res, y=y_res, curve=self.curve)
        elif isinstance(other, IdentityEllipticPoint):
            return self
        else:
            raise AttributeError(f'Wrong type for second point. Please specify EllipticPoint as <other>')

    def __pow__(self, power, modulo=None):
        """
        Перегрузка оператора возведения в степень
        Parameters
        ----------
        power : int
            Степень
        modulo : None
            deprecated

        Returns
        -------
        Union[EllipticPoint, IdentityEllipticPoint, gmpy2.mpz]
            Точка или делитель
        """
        power = bin(power)[2:][::-1]
        R = IdentityEllipticPoint(self.curve) if power[0] == '0' else self
        P = self
        for i in power:
            P = P + P
            if not is_point(P):
                return P
            if i == '1':
                R = R + P
                if not is_point(R):
                    return R
        return R
