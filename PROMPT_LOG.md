# Prompt Log (Vibe Coding)


## Prompt 1: Initial architecture

"Design a Hadoop-like distributed system using Docker with 1 master and 3 workers. Use static IP addresses and MapReduce-like communication."

---

## Prompt 2: Map/Reduce implementation

"Write Python code for a master that chunks CSV data, sends chunks to workers by IP over HTTP, and reduces partial results into final output."

---

## Prompt 3: Worker map logic

"Create worker Flask code that accepts chunk payload and returns partial aggregation for each chunk."
---

## Prompt 4: Fault tolerance

"How to simulate worker failure in Docker and reassign chunk processing to other workers automatically?"

- Added master failover loop for each chunk

---

## Prompt 5: Documentation and viva prep

"Generate concise architecture explanation, debugging report format, and viva-ready points for distributed MapReduce with Docker."

