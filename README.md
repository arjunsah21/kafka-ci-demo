# Kafka CI/CD Demo with Jenkins, Docker & Streamlit

## 📌 Overview

This project demonstrates a **production-style Kafka streaming system** with:

* Apache Kafka (3 brokers)
* ZooKeeper
* Jenkins CI/CD (Multibranch Pipeline)
* Docker & Docker Compose
* Python Kafka Producer
* Streamlit-based Kafka Consumer UI
* Prometheus + Grafana monitoring
* Kafka UI for topic inspection

Everything runs **locally on Docker Desktop** (no VMs).

---

## 🧠 Architecture

```
GitHub
  └── Jenkins Multibranch Pipeline
        ├── Build Docker Image
        ├── Deploy Kafka Producer
        └── Deploy Streamlit Consumer UI
              |
              v
        Kafka Cluster (Docker)
              |
      ┌───────┴────────┐
      │                │
 Kafka UI        Prometheus / Grafana
```

---

## 🗂️ Repository Structure

```
kafka-ci-demo/
├── Jenkinsfile
├── docker-compose.yml
├── README.md

├── python-client/
│   ├── producer.py
│   ├── consumer.py        # Streamlit-based consumer UI
│   ├── requirements.txt
│   └── Dockerfile

├── prometheus/
│   └── prometheus.yml

├── jenkins/
│   └── Dockerfile
```

---

## ⚙️ Prerequisites

* macOS / Linux
* Docker Desktop (8–12 GB RAM allocated)
* Git
* GitHub account

---

## 🧱 Infrastructure Setup (Docker Compose)

### Services provisioned

* ZooKeeper
* Kafka (3 brokers)
* Kafka UI
* Jenkins
* Prometheus
* Grafana

### Start infrastructure

```bash
docker compose up -d
```

### Verify running services

```bash
docker ps
```

---

## 🌐 Access URLs

| Service               | URL                                            |
| --------------------- | ---------------------------------------------- |
| Jenkins               | [http://localhost:8080](http://localhost:8080) |
| Kafka UI              | [http://localhost:8085](http://localhost:8085) |
| Prometheus            | [http://localhost:9090](http://localhost:9090) |
| Grafana               | [http://localhost:3000](http://localhost:3000) |
| Streamlit Consumer UI | [http://localhost:8501](http://localhost:8501) |

Grafana default credentials:

```
admin / admin
```

---

## 🧵 Kafka Details

* Topic: `demo-topic`
* Partitions: 3
* Replication factor: 3

### Create topic (if auto-create disabled)

```bash
docker exec kafka1 kafka-topics \
  --create \
  --topic demo-topic \
  --bootstrap-server kafka1:9092 \
  --partitions 3 \
  --replication-factor 3
```

---

## 🐍 Python Kafka Client

### Producer (`producer.py`)

* Continuously publishes messages to Kafka
* Deployed by Jenkins with CMD override

### Consumer (`consumer.py`)

* Streamlit UI
* Reads messages from Kafka
* Displays last 100 messages live
* Runs in its own consumer group

---

## 🐳 Docker Image Design

Single image: **`kafka-python-client`**

### Default behavior

Runs Streamlit UI:

```dockerfile
CMD ["streamlit", "run", "consumer.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Producer override at runtime

```bash
docker run kafka-python-client python producer.py
```

This pattern allows:

* One image
* Multiple roles
* Clean CI/CD control

---

## 🔁 CI/CD with Jenkins

### Jenkins runs inside Docker

* Docker socket mounted
* Jenkins runs as root (required on macOS)
* Builds & deploys containers directly

---

## 🔀 Jenkins Multibranch Pipeline (IMPORTANT)

This project **must use Multibranch Pipeline**.

Why:

* Jenkinsfile is loaded fresh per commit
* No cached pipelines
* Reliable GitHub integration

---

## 🛠️ Jenkins Setup Steps

1. Open Jenkins UI
2. **New Item**
3. Select **Multibranch Pipeline**
4. Branch Source → Git
5. Repo URL:

   ```
   https://github.com/<your-username>/kafka-ci-demo.git
   ```
6. Script Path:

   ```
   Jenkinsfile
   ```
7. Save
8. Click **Scan Multibranch Pipeline Now**

---

## 📜 Jenkinsfile (Key Logic)

### Build image

```groovy
docker build -t kafka-python-client ./python-client
```

### Deploy producer (CMD override)

```groovy
docker run -d \
  --name kafka-producer \
  --network kafka-ci-demo_kafka-net \
  kafka-python-client \
  python producer.py
```

### Deploy Streamlit consumer UI (default CMD)

```groovy
docker run -d \
  --name kafka-consumer \
  --network kafka-ci-demo_kafka-net \
  -p 8501:8501 \
  kafka-python-client
```

---

## 🔄 CI/CD Workflow

1. Modify `producer.py` or `consumer.py`
2. Commit & push to GitHub
3. Jenkins automatically (or manually) builds
4. Old containers stopped
5. New containers deployed
6. Kafka remains untouched
7. Grafana & Streamlit reflect changes live

---

## 📊 Monitoring

### Prometheus

Scrapes:

* Kafka Exporter
* Broker & consumer metrics

### Grafana

Recommended dashboards:

* Kafka Exporter Overview
* Consumer Lag

---

## 🧪 Validation Checklist

```bash
docker logs kafka-producer
```

✔ Messages being produced

```bash
docker logs kafka-consumer
```

✔ Streamlit running

Kafka UI:
✔ Offsets increasing

Grafana:
✔ Consumer lag & throughput visible

---

## 🧨 Common Issues & Fixes

### Jenkins using old Jenkinsfile

➡ Use **Multibranch Pipeline**
➡ Run **Scan Multibranch Pipeline Now**

### `fatal: not in a git directory`

➡ Clear Jenkins Git cache:

```bash
docker exec jenkins rm -rf /var/jenkins_home/caches/git*
```

### Kafka hostname not resolving

➡ Ensure correct network:

```
kafka-ci-demo_kafka-net
```

---
## 📈 Monitoring with Prometheus & Grafana

This project includes **full Kafka monitoring** using **Prometheus + Grafana**, backed by **Kafka Exporter**.

### What is monitored

* Kafka broker availability
* Topic & partition metrics
* Consumer group lag
* Message throughput

This gives **real observability**, not fake demo graphs.

---

## 🧩 Monitoring Components

### Services involved

| Component      | Purpose                                    |
| -------------- | ------------------------------------------ |
| Kafka Exporter | Exposes Kafka metrics in Prometheus format |
| Prometheus     | Scrapes and stores metrics                 |
| Grafana        | Visualizes metrics via dashboards          |

---

## 🔌 Kafka Exporter

Kafka does **not** expose Prometheus metrics natively.
Kafka Exporter bridges that gap. Kafka Exporter service is written in docker-compose

Exporter endpoint:

```
http://kafka-exporter:9308/metrics
```

---

## 📡 Prometheus Configuration

### `prometheus/prometheus.yml`

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]

  - job_name: "kafka-exporter"
    static_configs:
      - targets: ["kafka-exporter:9308"]
```

This tells Prometheus to scrape Kafka metrics every **15 seconds**.

---

## ▶️ Starting Prometheus & Grafana

If infra is not running:

```bash
docker compose up -d prometheus grafana kafka-exporter
```

Verify Prometheus targets:

👉 [http://localhost:9090/targets](http://localhost:9090/targets)

You should see:

* `prometheus` → **UP**
* `kafka-exporter` → **UP**

If Kafka Exporter is **DOWN**, Kafka networking is wrong.

---

## 📊 Grafana Setup

### 1️⃣ Access Grafana

👉 [http://localhost:3000](http://localhost:3000)

Default login:

```
username: admin
password: admin
```

(Change password when prompted.)

---

### 2️⃣ Add Prometheus as Data Source

1. Go to **Settings → Data Sources**
2. Click **Add data source**
3. Select **Prometheus**
4. URL:

   ```
   http://prometheus:9090
   ```
5. Click **Save & Test**

You should see:

```
Data source is working
```

---

## 📥 Import Kafka Dashboards

Grafana dashboards are **not auto-created**.
You must import them once.

### Recommended dashboards (official & stable)

#### 🔹 Kafka Exporter Overview

* **Dashboard ID:** `721`
* Shows:

  * Broker count
  * Topic partitions
  * Message rates

#### 🔹 Kafka Consumer Lag

* **Dashboard ID:** `7589`
* Shows:

  * Consumer group lag
  * Per-topic lag
  * Partition-level insight

---

### Steps to import dashboards

1. Grafana → **Dashboards → Import**
2. Enter Dashboard ID (e.g. `721`)
3. Select Prometheus data source
4. Click **Import**
5. Repeat for `7589`

---

## ✅ What to Expect After Import

Once producer & consumer are running:

* Consumer lag updates in real time
* Lag spikes when consumer is stopped
* Lag drops when consumer resumes
* Throughput matches producer rate

This directly validates:

* Kafka correctness
* Consumer group behavior
* CI/CD redeploy impact

---

## 🔍 Useful Prometheus Queries

Try these in **Prometheus → Graph**:

```text
kafka_consumergroup_lag
```

```text
kafka_topic_partitions
```

```text
kafka_brokers
```

If these return data → monitoring is healthy.

---

## 🧠 Why This Monitoring Design

* Kafka Exporter → simple, low overhead
* No JMX complexity for demos
* Prometheus-native metrics
* Grafana dashboards reused from production setups

This is **exactly how many real teams monitor Kafka**.

---

## 🛑 Common Monitoring Issues

### ❌ No Kafka metrics in Grafana

* Kafka Exporter not running
* Prometheus target down
* Wrong Prometheus URL in Grafana

### ❌ Consumer lag always zero

* Consumer group name mismatch
* Consumer not running
* Topic mismatch

---

## 🎯 Monitoring in CI/CD Context

During Jenkins deployments:

* Producer restarts → throughput visible
* Consumer restarts → lag spike visible
* Confirms zero message loss
* Demonstrates operational awareness

This elevates the demo from **“code works”** to **“system behaves correctly”**.

---

## 🧠 Design Decisions (Interview-Ready)

* Docker over VMs → faster, reproducible
* Multibranch Pipeline → no stale Jenkinsfiles
* Single image, multi-role → clean deployment
* Streamlit consumer → real-time observability
* Separate infra & app lifecycle → production mindset

---

## 🚀 Possible Enhancements

* GitHub webhook triggers
* Image tagging with commit SHA
* Rollback stage
* Multiple topics selector in Streamlit
* Authentication for UI
* Schema Registry
* TLS / SASL Kafka security

---

## 🏁 Conclusion

This repository demonstrates a **realistic streaming system** with:

* Messaging
* Observability
* CI/CD automation
* UI visualization

It is intentionally designed to mirror **real-world engineering practices**, not tutorials.

