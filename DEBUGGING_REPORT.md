# Debugging Report

## 1) Worker unreachable from master

### Symptom

Master failed to send chunk requests and timed out.

### Cause

Containers were up but workers were not fully ready.

### Fix

- Added master health checks (`GET /health`)
- Added retry delay before starting map tasks

---

## 2) Inconsistent worker identification in logs

### Symptom

Logs did not clearly show which worker processed each chunk.

### Cause

Worker responses lacked identity metadata.

### Fix

- Added `WORKER_ID` env variable per worker
- Included worker ID and chunk ID in response payload

---

## 3) Fault tolerance not demonstrated initially

### Symptom

Failure of one worker stopped chunk processing.

### Cause

No reassignment logic existed in master.

### Fix

- Added failover loop per chunk
- If one worker fails, master retries same chunk on remaining workers

---

## 4) CSV aggregation issues

### Symptom

Some records failed numeric conversion.

### Cause

CSV rows can include malformed or missing numeric fields.

### Fix

- Added safe float parsing with exception handling
- Ignored invalid records instead of crashing the worker

---

## How AI Assistance Helped

- Proposed robust endpoint structure (`/health` + `/process`)
- Suggested chunk retry/failover pattern
- Accelerated debugging by rapidly generating edge-case handling ideas
- Helped produce structured documentation for assignment submission
