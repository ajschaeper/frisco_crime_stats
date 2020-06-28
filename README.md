# San Fransisco Crime Statistics

## How to run it

### Setting up the environment
`./start.sh` 

### Start producing
`python kafka_server.py`

### Consume messges
`spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.3.4 --master local[*] data_stream.py`

## Evidences

TODO

## Parameter evaluation

TODO 

1. How did changing values on the SparkSession property parameters affect the throughput and latency of the data?
2. What were the 2-3 most efficient SparkSession property key/value pairs? Through testing multiple variations on values, how can you tell these were the most optimal?


