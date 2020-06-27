import producer_server

KAFKA_BROKER_URL = "localhost:9092"
KAFKA_TOPIC_NAME = "com.udacity.streams.sf_crime_stats.from_json"
DATA_FILE_PATH = "./police-department-calls-for-service.json"

def run_kafka_server():
    input_file = DATA_FILE_PATH

    producer = producer_server.ProducerServer(
        input_file = input_file,
        topic = KAFKA_TOPIC_NAME,
        bootstrap_servers = KAFKA_BROKER_URL,
        client_id="kafka-producer-from-json-file"
    )

    return producer


def feed():
    print(f"Starting Kafka producer into broker \"{KAFKA_BROKER_URL}\"")
    producer = run_kafka_server()
    print(f"Producing data from \"{DATA_FILE_PATH}\" into \"{KAFKA_TOPIC_NAME}\"")
    producer.generate_data()


if __name__ == "__main__":
    feed()
