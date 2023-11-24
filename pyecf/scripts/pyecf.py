import logging

import typer

from ..lenstras_algo import LenstraAlgorithm

cli = typer.Typer()
logging.basicConfig(level=logging.INFO)


@cli.command()
def run_pyecf(
    n: int,
    omega: int = typer.Option(
        100,
        help='prime numbers` bound for generating power. Approximate time to spend for the factorization',
    ),
    nu: int = typer.Option(
        10000,
        help='power bound of prime numbers for generating power. Approximate upper bound for divisors',
    ),
):
    logging.info(f"Factorizing n = {n}")
    algo = LenstraAlgorithm(n, omega=omega, nu=nu)
    factors = algo.factorize()
    if algo.check_factorization(factors):
        logging.info(f"{n} = {'*'.join(list(map(str, factors)))}")
    else:
        logging.error('Factorization failed')


if __name__ == '__main__':
    cli()
