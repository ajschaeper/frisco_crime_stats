# define environment

ZOOKEEPER_CONFIG_FILE="./config/zookeeper.properties"
ZOOKEEPER_HOST="localhost"
ZOOKEEPER_PORT=$(cat ${ZOOKEEPER_CONFIG_FILE} | grep ^clientPort= | awk -F "=" '{print $2}')
ZOOKEEPER_URL=${ZOOKEEPER_HOST}:${ZOOKEEPER_PORT}

KAFKA_CONFIG_FILE="./config/server.properties"
KAFKA_BROKER_HOST="localhost"
KAFKA_BROKER_PORT=$(cat ${KAFKA_CONFIG_FILE} | grep ^port= | awk -F "=" '{print $2}')
KAFKA_BROKER_URL=${KAFKA_BROKER_HOST}:${KAFKA_BROKER_PORT}
KAFKA_TOPIC_NAME="com.udacity.streams.sf_crime_stats.from_json"

# set handy shortcuts for kafka cli tools
alias kts="kafka-topics --zookeeper ${ZOOKEEPER_URL}"
alias kcp="kafka-console-producer --broker-list ${KAFKA_BROKER_URL}"
alias kcc="kafka-console-consumer --bootstrap-server ${KAFKA_BROKER_URL}"

# start zookeeper
echo -n "> Starting ZooKeeper at ${ZOOKEEPER_URL} ... "
zookeeper-server-start ${ZOOKEEPER_CONFIG_FILE} 1> /tmp/zookeeper.out 2> /tmp/zookeeper.err &
sleep 17
echo "done"

# start kafka
echo -n "> Starting Kafka at ${KAFKA_BROKER_URL} ... "
kafka-server-start ${KAFKA_CONFIG_FILE} 1> /tmp/kafka.out 2> /tmp/kafka.err &

echo "done"
# install python deps
echo "> Installing Python dependencties with Conda"
conda install -y --file requirements.txt

# create kafka topic
echo "> Creating Kafka topic"
kafka-topics --zookeeper ${ZOOKEEPER_URL} --create --partitions 1 --replication-factor 1 --topic ${KAFKA_TOPIC_NAME} 


# EOF
