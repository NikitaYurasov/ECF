def full_power(n):
    """
    Функция нахождения нахождения наибольшей степени и основания для заданного числа

    n = base ^ power : power --> max, base --> min

    Parameters
    ----------
    n : Union[gmpy2.mpz, int]
        Число

    Returns
    -------
    Tuple[int, Union[gmpy2.mpz, int]]
        Максимальная степень, минимальное основание
    """
    power = 1
    base = n
    right_bound = n
    i = 2
    while right_bound > 2:
        if (abs(n ** (1 / i)) - round(n ** (1 / i))) < 1e-8:
            if round(n ** (1 / i)) ** i == n:
                power = i
                base = round(n ** (1 / i))
        right_bound = n ** (1 / i)
        i += 1
    return power, base
