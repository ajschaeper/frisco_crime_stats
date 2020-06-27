echo "> Installing Python dependencties with Conda"
conda install -y --file requirements.txt

echo -n "> Starting ZooKeeper at localhost:2181 ... "
zookeeper-server-start config/zookeeper.properties 1> /tmp/zookeeper.out 2> /tmp/zookeeper.err &
sleep 17
echo "done"

echo -n "> Starting Kafka at localhost:9092 ... "
kafka-server-start config/server.properties 1> /tmp/kafka.out 2> /tmp/kafka.err &
echo "done"

# EOF
