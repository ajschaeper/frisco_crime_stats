# set handy shortcuts for kafka cli tools
alias kts="kafka-topics --zookeeper localhost:2181"
alias kcp="kafka-console-producer --broker-list localhost:9092"
alias kcc="kafka-console-consumer --bootstrap-server localhost:9092"

# install python deps
echo "> Installing Python dependencties with Conda"
conda install -y --file requirements.txt

# start zookeeper
echo -n "> Starting ZooKeeper at localhost:2181 ... "
zookeeper-server-start config/zookeeper.properties 1> /tmp/zookeeper.out 2> /tmp/zookeeper.err &
sleep 17
echo "done"

# start kafka
echo -n "> Starting Kafka at localhost:9092 ... "
kafka-server-start config/server.properties 1> /tmp/kafka.out 2> /tmp/kafka.err &
sleep 17
echo "done"


# EOF