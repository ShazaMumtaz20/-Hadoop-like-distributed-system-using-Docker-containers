# worker/worker.py
import os
import re
from collections import Counter
from statistics import mean

from flask import Flask, jsonify, request

app = Flask(__name__)

TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9']+")
WORKER_ID = os.getenv("WORKER_ID", "worker-unknown")
SIMULATE_FAILURE = os.getenv("SIMULATE_FAILURE", "false").lower() == "true"


@app.get("/health")
def health():
    return jsonify({"status": "ok", "worker_id": WORKER_ID}), 200


@app.post("/process")
def process():
    payload = request.get_json(silent=True) or {}
    task_type = payload.get("task_type", "word_count")
    chunk_id = payload.get("chunk_id", "unknown")
    chunk = payload.get("chunk", [])

    if SIMULATE_FAILURE:
        return jsonify({"status": "error", "message": f"{WORKER_ID} simulated failure"}), 500

    if task_type == "word_count":
        tokens = []
        for line in chunk:
            if not isinstance(line, str):
                continue
            tokens.extend([token.lower() for token in TOKEN_PATTERN.findall(line)])
        result = dict(Counter(tokens))
    elif task_type == "price_sum":
        values = []
        for row in chunk:
            if isinstance(row, dict):
                try:
                    values.append(float(row.get("RetailPrice", 0)))
                except (TypeError, ValueError):
                    continue
        result = {
            "sum_retail_price": round(sum(values), 4),
            "count": len(values),
            "avg_retail_price": round(mean(values), 4) if values else 0.0,
        }
    else:
        return jsonify({"status": "error", "message": f"unsupported task_type: {task_type}"}), 400

    return jsonify(
        {
            "status": "success",
            "worker_id": WORKER_ID,
            "chunk_id": chunk_id,
            "task_type": task_type,
            "result": result,
        }
    ), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)