import os
import logging
from dotenv import load_dotenv
import click
from requests import get

logging.basicConfig(level=logging.INFO)
load_dotenv()

def ping_service_seq(urls: list[str]) -> list[str]:
    """Ping the service sequentially"""
    responses = []

    for url in urls:
        response = get(url)
        logging.info(f"Response: {response.text}")
        responses.append(response.text)

    return responses

@click.command()
@click.option("--limit", default=20, help="Number of elements in the array")
@click.option("--mode", default="sequential", help="Mode of execution")
def run(limit: int, mode: str):
    urls = [os.getenv("HTTP_ENDPOINT")] * limit

    match mode:
        case "sequential":
            print(ping_service_seq(urls))
        case _:
            raise ValueError("Invalid mode provided")

if __name__ == "__main__":
    run()
