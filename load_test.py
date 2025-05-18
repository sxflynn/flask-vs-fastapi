import argparse
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

def send_request(url, index):
    try:
        start = time.time()
        response = requests.post(url, timeout=10)
        duration = time.time() - start
        response.raise_for_status()
        print(f"[✓] Request {index+1} succeeded in {duration:.2f}s")
        return response.text
    except Exception as e:
        print(f"[✗] Request {index+1} failed: {e}")
        return f"ERROR: {e}"

def main():
    parser = argparse.ArgumentParser(
        description="Fire concurrent POST requests and measure total time."
    )
    parser.add_argument("--url", required=True,
                        help="Endpoint to hit, e.g. http://localhost:8080/process")
    parser.add_argument("--requests", type=int, default=10,
                        help="Total number of POST requests to send")
    parser.add_argument("--concurrency", type=int, default=10,
                        help="Number of concurrent threads")
    args = parser.parse_args()

    print(f"Starting load test:")
    print(f"- Target URL: {args.url}")
    print(f"- Total requests: {args.requests}")
    print(f"- Concurrency level: {args.concurrency}")
    print("------------------------------------------------------------")

    start_time = time.time()

    results = []
    with ThreadPoolExecutor(max_workers=args.concurrency) as executor:
        futures = [
            executor.submit(send_request, args.url, i)
            for i in range(args.requests)
        ]
        for future in as_completed(futures):
            results.append(future.result())

    total_duration = time.time() - start_time

    print("------------------------------------------------------------")
    print(f"\nFinished in {total_duration:.2f} seconds")
    expected_response = "Took 2 seconds"
    success_count = sum(1 for res in results if res == expected_response)
    print(f"✔️  {success_count}/{args.requests} responses matched expected text")

    if success_count != args.requests:
        print("\nFailed or unexpected responses:")
        for i, res in enumerate(results):
            if res != expected_response:
                print(f"  #{i+1}: {res}")

if __name__ == "__main__":
    main()
