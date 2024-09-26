import os
import logging
from itertools import batched
from dotenv import load_dotenv
import click
from requests import get

logging.basicConfig(level=logging.INFO)
load_dotenv()

def ping_service_seq(urls: list[str], thread_name:str="") -> list[str]:
    """Ping the service sequentially"""
    responses = []

    for url in urls:
        response = get(url)
        logging.info(f"Response: {response.text} via {thread_name}")
        responses.append(response.text)

    return responses

def ping_service_multiprocessing(urls: list[str], cores:int) -> list[str]:
    """Ping the service using multiprocessing"""
    from multiprocessing import Pool

    chunk_size = len(urls) // cores
    chunks = batched(urls, chunk_size)

    results = []

    with Pool(processes=cores) as pool:
        process_pool = pool.imap(ping_service_seq, chunks)

        for result in process_pool:
            results.extend(result)

    return results

def ping_service_multithreading(urls: list[str], threads:int) -> list[str]:
    """Ping the service using multithreading"""
    from threading import Thread

    chunk_size = len(urls) // threads
    chunks = batched(urls, chunk_size)

    results = []

    class PingThread(Thread):
        def __init__(self, chunk):
            super().__init__()
            self.chunk = chunk
            self.value = []

        def run(self):
            self.value = ping_service_seq(self.chunk, self.name)

    threads = []
    for chunk in chunks:
        thread = PingThread(chunk)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
        results.extend(thread.value)

    return results

@click.command()
@click.option("--limit", default=400, help="Number of elements in the array")
@click.option("--mode", default="sequential", help="Mode of execution")
def run(limit: int, mode: str):
    urls = [os.getenv("HTTP_ENDPOINT")] * limit

    import time
    start = time.time()
    match mode:
        case "sequential":
            print(ping_service_seq(urls))
        case "multithreading":
            print(ping_service_multithreading(urls, 20))
        case "multiprocessing":
            cores = os.cpu_count()
            print(ping_service_multiprocessing(urls, cores))
        case _:
            raise ValueError("Invalid mode provided")

    print(f"Total running time: {time.time() - start}")

if __name__ == "__main__":
    # Measure the time taken to run the program
    run()
