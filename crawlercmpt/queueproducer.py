from kafka import KafkaProducer
import json

class QueueProducer:
    def __init__(self, brokens):
        self.producer = KafkaProducer(
            bootstrap_servers=brokens,
            value_serializer=lambda m: json.dumps(m).encode("ascii"),
        )

    def publish(self, topic, key_values):
        self.producer.send(topic, key_values)

