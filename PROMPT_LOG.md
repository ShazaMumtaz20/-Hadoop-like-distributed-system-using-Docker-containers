# Prompt Log (Vibe Coding)

Use this file as your submission prompt log. You can keep these prompts exactly as used or adapt with your own chat history.

## Prompt 1: Initial architecture

"Design a Hadoop-like distributed system using Docker with 1 master and 3 workers. Use static IP addresses and MapReduce-like communication."

### AI Output Used

- Suggested master-worker split
- Suggested Docker bridge network with fixed IPs

### Change Made

- Added explicit `/health` and `/process` endpoints for worker APIs

---

## Prompt 2: Map/Reduce implementation

"Write Python code for a master that chunks CSV data, sends chunks to workers by IP over HTTP, and reduces partial results into final output."

### AI Output Used

- Master orchestration logic
- Chunking and reducer templates

### Change Made

- Added `price_sum` reducer fields (sum/count/average)
- Added output JSON persistence

---

## Prompt 3: Worker map logic

"Create worker Flask code that accepts chunk payload and returns partial aggregation for each chunk."

### AI Output Used

- Base Flask route structure

### Change Made

- Added support for multiple task types (`price_sum`, `word_count`)
- Added worker identity metadata (`WORKER_ID`)

---

## Prompt 4: Fault tolerance

"How to simulate worker failure in Docker and reassign chunk processing to other workers automatically?"

### AI Output Used

- Failure simulation using env variable
- Retry strategy suggestion

### Change Made

- Implemented `SIMULATE_FAILURE` in worker
- Added master failover loop for each chunk

---

## Prompt 5: Documentation and viva prep

"Generate concise architecture explanation, debugging report format, and viva-ready points for distributed MapReduce with Docker."

### AI Output Used

- Structured report sections
- Typical troubleshooting checklist

### Change Made

- Customized using actual file names, endpoints, and dataset
