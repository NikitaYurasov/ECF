import argparse

from lenstas_algo import LenstraAlgorithm
from logger import logger

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Small hits to start factorizing")
    parser.add_argument('-n', '--number', help='number to factorize by ECF Method', required=True)
    args = parser.parse_args()
    log = logger.setup_applevel_logger()
    n = int(args.number)
    print(f"Factorizing n = {n}")
    algo = LenstraAlgorithm(n)
    factors = algo.factorize()
    if algo.check_factorization(factors):
        print(f"{n} = {'*'.join(list(map(str, factors)))}")
