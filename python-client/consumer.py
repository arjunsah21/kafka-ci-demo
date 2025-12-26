import streamlit as st
from kafka import KafkaConsumer
import time

st.set_page_config(
    page_title="Kafka Consumer",
    layout="wide"
)

st.title("📡 Kafka Consumer – Live Messages")

@st.cache_resource
def get_consumer():
    return KafkaConsumer(
        "demo-topic",
        bootstrap_servers=["kafka1:9092"],
        group_id="streamlit-consumer-group",
        auto_offset_reset="latest",
        value_deserializer=lambda v: v.decode("utf-8"),
        enable_auto_commit=True
    )

consumer = get_consumer()

message_box = st.empty()
messages = []

while True:
    records = consumer.poll(timeout_ms=1000)

    for tp, msgs in records.items():
        for msg in msgs:
            messages.append(msg.value)
            messages = messages[-100:]  # keep last 100

    with message_box.container():
        for m in reversed(messages):
            st.write(m)

    time.sleep(1)
