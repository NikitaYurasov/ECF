def full_power(n):
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
