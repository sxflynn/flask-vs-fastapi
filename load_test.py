import argparse
import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple

import requests

# -----------------------------------------------------------------------------
# Configuration Defaults
# -----------------------------------------------------------------------------

DEFAULT_NUM_REQUESTS = 10
DEFAULT_CONCURRENCY = 10
DEFAULT_TIMEOUT = 10
DEFAULT_EXPECTED_RESPONSE = "Took 2 seconds"

# -----------------------------------------------------------------------------
# Logging Setup
# -----------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
# Core Logic
# -----------------------------------------------------------------------------

def send_post_request(url: str, index: int, timeout: int) -> Tuple[bool, str]:
    """
    Sends a single POST request.

    Args:
        url: The target endpoint.
        index: The request index (0-based).
        timeout: Timeout in seconds for the request.

    Returns:
        Tuple of (success_flag, response_text or error)
    """
    try:
        start_time = time.time()
        response = requests.post(url, timeout=timeout)
        duration = time.time() - start_time
        response.raise_for_status()
        logger.info(f"[✓] Request #{index + 1} succeeded in {duration:.2f}s")
        return True, response.text
    except Exception as e:
        logger.error(f"[✗] Request #{index + 1} failed: {e}")
        return False, f"ERROR: {e}"

def run_load_test(
    url: str,
    num_requests: int,
    concurrency: int,
    timeout: int,
    expected_response: str
) -> None:
    """
    Executes a load test with the given configuration.

    Args:
        url: Target URL to send POST requests to.
        num_requests: Total number of requests to send.
        concurrency: Number of concurrent threads to use.
        timeout: Timeout for each request.
        expected_response: Expected response text to verify success.
    """
    logger.info("------------------------------------------------------------")
    logger.info("Load Test Configuration:")
    logger.info(f"- Target URL: {url}")
    logger.info(f"- Total requests: {num_requests}")
    logger.info(f"- Concurrency: {concurrency}")
    logger.info(f"- Timeout per request: {timeout}s")
    logger.info(f"- Expected response: {expected_response}")
    logger.info("------------------------------------------------------------")

    start_time = time.time()

    results: List[str] = []
    successes = 0

    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [
            executor.submit(send_post_request, url, i, timeout)
            for i in range(num_requests)
        ]
        for future in as_completed(futures):
            success, result = future.result()
            results.append(result)
            if success and result == expected_response:
                successes += 1

    duration = time.time() - start_time
    logger.info("------------------------------------------------------------")
    logger.info(f"Finished in {duration:.2f} seconds")
    logger.info(f"✔️  {successes}/{num_requests} responses matched expected response")

    if successes != num_requests:
        logger.warning("Some responses did not match expected output:")
        for i, res in enumerate(results):
            if res != expected_response:
                logger.warning(f"  #{i + 1}: {res}")

# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Concurrent POST load tester")
    parser.add_argument("--url", required=True, help="Target URL to POST to")
    parser.add_argument("--requests", type=int, default=DEFAULT_NUM_REQUESTS,
                        help="Total number of requests to send")
    parser.add_argument("--concurrency", type=int, default=DEFAULT_CONCURRENCY,
                        help="Number of concurrent threads")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT,
                        help="Timeout (in seconds) for each request")
    parser.add_argument("--expected-response", type=str,
                        default=DEFAULT_EXPECTED_RESPONSE,
                        help="Expected exact response string for success")
    return parser.parse_args()

# -----------------------------------------------------------------------------
# Entry Point
# -----------------------------------------------------------------------------

def main() -> None:
    args = parse_args()
    run_load_test(
        url=args.url,
        num_requests=args.requests,
        concurrency=args.concurrency,
        timeout=args.timeout,
        expected_response=args.expected_response,
    )

if __name__ == "__main__":
    main()
