""" Check if a number is prime or not using sequential, multithreading, and multiprocessing """

import os
from itertools import batched
from typing import List
import random
from viztracer import VizTracer
import click


def is_prime(n):
    """Check if a number is prime or not"""
    for i in range(2, n):
        if n % i == 0:
            return (n, False)
    return (n, True)


def generate_data(limit: int):
    """Generate random data"""
    return [random.randint(10000, 100000) for i in range(limit)]


def check_prime_numbers(arr: List[int]):
    """Check if the numbers in the array are prime or not, runs sequentially"""
    return [is_prime(elem) for elem in arr]


def check_prime_numbers_multiprocessing(arr: List[int], cores: int = os.cpu_count()):
    """Check if the numbers in the array are prime or not, runs using multiprocessing"""
    from multiprocessing import Pool

    chunk_size = len(arr) // cores
    chunks = batched(arr, chunk_size)

    results = []

    with Pool(processes=cores) as pool:
        process_pool = pool.imap(check_prime_numbers, chunks)

        for result in process_pool:
            results.extend(result)

    return results


def check_prime_numbers_multithreading(arr: List[int], threads: int = 8):
    """Check if the numbers in the array are prime or not, runs using multithreading"""
    from threading import Thread

    chunk_size = len(arr) // threads
    chunks = batched(arr, chunk_size)

    results = []

    class PrimeNumberThread(Thread):
        def __init__(self, chunk):
            super().__init__()
            self.chunk = chunk
            self.value = []

        def run(self):
            self.value = check_prime_numbers(self.chunk)

    threads = []
    for chunk in chunks:
        thread = PrimeNumberThread(chunk)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
        results.extend(thread.value)

    return results


@click.command()
@click.option("--limit", default=60000, help="Number of elements in the array")
@click.option("--mode", default="sequential", help="Mode of execution")
def run(limit: int, mode: str):
    # Generate random data
    num_arr = generate_data(limit)

    import time

    start = time.time()
    match mode:
        case "sequential":
            check_prime_numbers(num_arr)
        case "multithreading":
            check_prime_numbers_multithreading(num_arr)
        case "multiprocessing":
            check_prime_numbers_multiprocessing(num_arr)
        case _:
            raise ValueError("Invalid mode provided")

    print(f"Time taken: {time.time() - start}")


if __name__ == "__main__":
    run()
