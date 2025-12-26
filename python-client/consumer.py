from kafka import KafkaConsumer

consumer = KafkaConsumer(
    "demo-topic",
    bootstrap_servers=["kafka1:9092"],
    auto_offset_reset="earliest",
    group_id="demo-group",
    value_deserializer=lambda v: v.decode("utf-8")
)

for msg in consumer:
    print("Received:", msg.value)
