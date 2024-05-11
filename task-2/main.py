import logging
import concurrent.futures
from multiprocessing import cpu_count
from time import time


def factorize_single(number):
    num_factors = []
    for i in range(1, number + 1):
        if number % i == 0:
            num_factors.append(i)
    return num_factors


def factorize(*numbers):
    factors = []
    for number in numbers:
        factors.append(factorize_single(number))
    return factors


def multi_factorize(*numbers):
    with concurrent.futures.ProcessPoolExecutor(max_workers=cpu_count()) as executor:
        return list(executor.map(factorize_single, numbers))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    timer = time()
    result = factorize(128, 255, 99999, 10651060)

    logging.info(f"{result}")
    logging.info(f"Done single process: {round(time() - timer, 4)}")

    timer_multi = time()
    result_multi = multi_factorize(128, 255, 99999, 10651060)

    logging.info(f"{result_multi}")
    logging.info(f"Done multi process: {round(time() - timer_multi, 4)}")
