from config import (
    BOOTSTRAP_SERVER,
    TOPIC_NAME
)

from kafka_producer import IDSKafkaProducer


producer = IDSKafkaProducer(
    BOOTSTRAP_SERVER,
    TOPIC_NAME
)

producer.send({

    "message": "Kafka Test",

    "status": "working"

})

producer.flush()

producer.close()

print("✅ Kafka Producer Test Passed")