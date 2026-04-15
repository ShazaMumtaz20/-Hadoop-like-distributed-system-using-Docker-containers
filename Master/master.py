import csv
import json
import os
from collections import Counter
from pathlib import Path
from time import sleep

import requests

DATASET_PATH = Path(os.getenv("DATASET_PATH", "/data/Fruit Prices 2022.csv"))
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "/data/output"))
TASK_TYPE = os.getenv("TASK_TYPE", "price_sum")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "20"))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "5"))

WORKERS = [
    {"id": "worker1", "ip": "172.20.0.11", "port": 5000},
    {"id": "worker2", "ip": "172.20.0.12", "port": 5000},
    {"id": "worker3", "ip": "172.20.0.13", "port": 5000},
]


def wait_for_worker(worker, retries=10, delay=2):
    url = f"http://{worker['ip']}:{worker['port']}/health"
    for _ in range(retries):
        try:
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
            if response.status_code == 200:
                return True
        except requests.RequestException:
            pass
        sleep(delay)
    return False


def load_dataset(task_type):
    if task_type == "word_count":
        with DATASET_PATH.open("r", encoding="utf-8") as file:
            return [line.strip() for line in file if line.strip()]
    if task_type == "price_sum":
        with DATASET_PATH.open("r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return list(reader)
    raise ValueError(f"Unsupported TASK_TYPE: {task_type}")


def chunk_data(data, chunk_size):
    return [data[i : i + chunk_size] for i in range(0, len(data), chunk_size)]


def send_chunk_to_worker(worker, chunk_id, chunk, task_type):
    url = f"http://{worker['ip']}:{worker['port']}/process"
    payload = {"chunk_id": chunk_id, "task_type": task_type, "chunk": chunk}
    response = requests.post(url, json=payload, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    parsed = response.json()
    if parsed.get("status") != "success":
        raise RuntimeError(f"Worker error from {worker['id']}: {parsed}")
    return parsed


def process_with_failover(chunks, available_workers, task_type):
    partial_results = []
    for index, chunk in enumerate(chunks):
        chunk_id = f"chunk-{index + 1}"
        assigned_order = [
            available_workers[index % len(available_workers)],
            *[w for w in available_workers if w != available_workers[index % len(available_workers)]],
        ]
        success = False

        for worker in assigned_order:
            try:
                result = send_chunk_to_worker(worker, chunk_id, chunk, task_type)
                partial_results.append(result)
                print(f"[OK] {chunk_id} processed by {worker['id']} ({worker['ip']})")
                success = True
                break
            except Exception as error:
                print(f"[WARN] {chunk_id} failed on {worker['id']} ({worker['ip']}): {error}")

        if not success:
            raise RuntimeError(f"All workers failed for {chunk_id}")

    return partial_results


def reduce_results(partial_results, task_type):
    if task_type == "word_count":
        aggregated = Counter()
        for item in partial_results:
            aggregated.update(item["result"])
        return dict(aggregated)

    if task_type == "price_sum":
        total_sum = 0.0
        total_count = 0
        for item in partial_results:
            chunk_result = item["result"]
            total_sum += chunk_result.get("sum_retail_price", 0.0)
            total_count += chunk_result.get("count", 0)
        return {
            "global_sum_retail_price": round(total_sum, 4),
            "global_count": total_count,
            "global_avg_retail_price": round(total_sum / total_count, 4) if total_count else 0.0,
        }

    raise ValueError(f"Unsupported TASK_TYPE: {task_type}")


def write_output(task_type, chunks, partial_results, final_result):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = OUTPUT_DIR / f"result_{task_type}.json"
    data = {
        "task_type": task_type,
        "dataset": str(DATASET_PATH),
        "total_chunks": len(chunks),
        "partial_results": partial_results,
        "final_result": final_result,
    }
    with output_file.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)
    return output_file


def main():
    if not DATASET_PATH.exists():
        raise FileNotFoundError(f"Dataset not found at: {DATASET_PATH}")

    ready_workers = [worker for worker in WORKERS if wait_for_worker(worker)]
    if not ready_workers:
        raise RuntimeError("No workers are reachable. Check container IP/network settings.")
    print(f"[INFO] Ready workers: {[worker['id'] for worker in ready_workers]}")

    data = load_dataset(TASK_TYPE)
    chunks = chunk_data(data, CHUNK_SIZE)
    print(f"[INFO] Dataset rows/lines: {len(data)} | chunks: {len(chunks)} | task: {TASK_TYPE}")

    partial_results = process_with_failover(chunks, ready_workers, TASK_TYPE)
    final_result = reduce_results(partial_results, TASK_TYPE)
    output_file = write_output(TASK_TYPE, chunks, partial_results, final_result)

    print(f"[DONE] Final reduced output: {final_result}")
    print(f"[DONE] Saved output to: {output_file}")


if __name__ == "__main__":
    main()
