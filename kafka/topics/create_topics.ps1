docker exec kafka /opt/kafka/bin/kafka-topics.sh --create --topic raw-traffic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

docker exec kafka /opt/kafka/bin/kafka-topics.sh --create --topic clean-traffic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

docker exec kafka /opt/kafka/bin/kafka-topics.sh --create --topic selected-features --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

docker exec kafka /opt/kafka/bin/kafka-topics.sh --create --topic classification-results --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

docker exec kafka /opt/kafka/bin/kafka-topics.sh --create --topic unknown-traffic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

docker exec kafka /opt/kafka/bin/kafka-topics.sh --create --topic alerts --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1