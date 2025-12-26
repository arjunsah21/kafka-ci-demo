from kafka import KafkaProducer
import time

producer = KafkaProducer(
    bootstrap_servers=["kafka1:9092"],
    value_serializer=lambda v: v.encode("utf-8")
)

i = 0
while True:
    msg = f"message-{i}"
    producer.send("demo-topic", msg)
    print("Sent:", msg)
    i += 1
    time.sleep(2)
