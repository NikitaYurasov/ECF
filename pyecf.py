import argparse

from lenstras_algo import LenstraAlgorithm
from logger import logger

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Small hits to start factorizing")
    parser.add_argument('-n', '--number', help='number to factorize by ECF Method', required=True)
    parser.add_argument(
        '-w',
        '--omega',
        help='prime numbers` bound for generating power\n' 'Approx time to spend for the factorization',
        required=False,
    )
    parser.add_argument(
        '-v',
        '--nu',
        help='power bound of prime numbers for generating power\n' 'Approx upper bound for divisors',
        required=False,
    )
    args = parser.parse_args()
    log = logger.setup_applevel_logger()
    n = int(args.number)
    omega = int(args.omega) if args.omega is not None else args.omega
    nu = int(args.nu) if args.nu is not None else args.nu
    print(f"Factorizing n = {n}")
    algo = LenstraAlgorithm(n, omega=omega, nu=nu)
    factors = algo.factorize()
    if algo.check_factorization(factors):
        print(f"{n} = {'*'.join(list(map(str, factors)))}")
    else:
        log.error('Factorization failed')
