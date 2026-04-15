# Big Data Analytics Assignment

This project simulates a Hadoop-like distributed system using Docker containers and IP-based communication.

## Implemented Requirements

- 1 Master node (`master`, IP `172.20.0.10`)
- 3 Worker nodes (`worker1/2/3`, IPs `172.20.0.11`, `172.20.0.12`, `172.20.0.13`)
- Data chunking by master (`CHUNK_SIZE` configurable)
- Map phase on workers (`/process` endpoint)
- Reduce phase on master (aggregate final output)
- Optional advanced feature: node failure simulation + task reassignment

## Project Structure

- `Master/master.py`: orchestrates chunking, worker communication, reduce, and output
- `Master/Dockerfile.txt`: builds master image
- `Master/Data/Fruit Prices 2022.csv`: dataset
- `Worker/worker.py`: worker API for map tasks
- `Worker/Dockerfile.txt`: builds worker image
- `docker-compose.yml`: multi-container cluster and static IP network
- `Master/Data/output/result_price_sum.json`: generated final output after run

## How It Works (MapReduce Flow)

1. `master` waits for healthy workers using `GET /health`
2. Master reads dataset and splits into chunks
3. Each chunk is sent to a worker by direct IP (`POST /process`)
4. Workers return partial results
5. Master reduces all partial outputs into one final result JSON

## Run Instructions

From the project root:

```bash
docker compose up --build
```

After completion, check:

- Output JSON: `Master/Data/output/result_price_sum.json`
- Logs: `docker compose logs master`

Stop and clean:

```bash
docker compose down
```

## Optional Advanced: Simulate Worker Failure

To simulate failure on one worker, edit `docker-compose.yml`:

- Set `SIMULATE_FAILURE=true` for `worker2` (or any worker)

Then rerun:

```bash
docker compose up --build
```

Master will automatically retry failed chunks on another available worker (task reassignment).

## Notes for Viva

- Static IPs prove explicit node-to-node communication.
- Master performs chunking + scheduling + reduce.
- Workers are stateless map executors.
- Failover logic demonstrates distributed fault tolerance basics.
