# GreenRoute AI: Enterprise Carbon-Aware LLM Proxy

GreenRoute AI is an intelligent, high-performance, carbon-aware proxy architecture built to dynamically route Large Language Model (LLM) requests. By conducting real-time cognitive weight evaluations, GreenRoute AI automatically intercepts incoming prompt payloads and routes them to either high-efficiency local Small Language Models (SLMs) running on edge/containerized hardware, a low-latency semantic caching plane, or scales out to heavy cloud-hosted foundational LLMs.

The goal is minimizing hardware carbon footprint calculations ($g\text{ CO}_2e$) without breaking SLA response latencies.

---

## ⚡ Core Architecture Features

* **Dynamic Cognitive Weight Classifier:** Intercepts prompt tokens and runs real-time complexity matrix calculations via an approximate nearest neighbors semantic search loop to assess compute costs before selecting hardware runtimes.
* **Multi-Tier Automated Load Balancing:**
* **Tier 1: Semantic Cache Plane:** Near-zero carbon footprint lookup layer matching historical request vectors.
* **Tier 2: Local SLM Offload:** Local-host execution bounds for standard cognitive tasks to completely eliminate cloud transit energy drain.
* **Tier 3: Cloud LLM Integration:** Strategic execution routing for high-complexity, deep reasoning requests.


* **Dual-Theme Telemetry Dashboard Console:** A premium, high-contrast operations panel mapping dynamic network topology ratios, active proxy ports (`8080`), and total cumulative environmental mitigation figures ($g\text{ CO}_2$). Equipped with native system toggles for obsidian-dark and high-readability industrial-light workspaces.

---

## 🛠️ System Technology Stack

* **Backend Engine:** Python, FastAPI, Uvicorn asynchronous workers.
* **Containerization:** Docker, Multi-Stage Build `Dockerfiles`, Docker Compose orchestration.
* **Frontend Analytics Terminal:** HTML5, Tailwind CSS, Lucide Workflow Icons, Native JS Fetch Core.

---

## 📂 Project Repository Layout

```text
├── Dockerfile                  # Production-grade multi-stage container manifest
├── docker-compose.yml          # Persistent container cluster stack mappings
├── requirements.txt            # Explicit backend environment dependencies
└── src/
    ├── main.py                 # Core FastAPI engine & proxy telemetry loop paths
    └── static/
        └── index.html          # High-performance multi-theme dashboard UI

```

---

## 🚀 Local Deployment and Standup

### Prerequisites

* Ensure Docker and Docker Compose (v2.0+) are installed on your system node.

### 1. Build and Run the Stack

Spin up the containerized network environment using Docker Compose. The local source directory is bound dynamically to allow real-time layout asset updates without breaking container persistence:

```bash
docker compose up -d --build

```

### 2. Verify Infrastructure State

Confirm your backend router container instance successfully mapped incoming networking binds to port `8080`:

```bash
docker compose ps

```

### 3. Accessing the Telemetry Interface

Open your browser and navigate to the operational sandbox dashboard:

* **Terminal UI Access:** [http://localhost:8080/](https://www.google.com/search?q=http://localhost:8080/) or [http://127.0.0.1:8080/](http://127.0.0.1:8080/)

---

## 🔌 API Endpoints Reference Specification

### 1. Execute Chat Completions

Forwards prompt payloads downstream into the evaluation classification routing framework.

* **Endpoint:** `POST /v1/chat/completions`
* **Payload Format:**

```json
{
  "prompt": "Optimize a high-throughput microservices message broker layout using Docker containers."
}

```

* **Success Response Schema (`200 OK`):**

```json
{
  "response": "Generated content string response buffer output...",
  "route": "Local-SLM",
  "complexity_tier": "Medium-Structural",
  "latency_ms": 342,
  "carbon_emitted_g": 0.00142
}

```

### 2. Live Telemetry Summary Statistics

Retrieves cumulative ecosystem performance calculations. Used by the dashboard UI every 5 seconds for live pooling updates.

* **Endpoint:** `GET /api/stats`
* **Success Response Schema (`200 OK`):**

```json
{
  "total_carbon_saved_g": 42.8912,
  "total_requests": 154,
  "cache_hits": 38,
  "local_slm_routes": 92,
  "cloud_llm_routes": 24
}

```

---

## 🔄 Git Development Workflow Strategy

To safely commit dashboard refinements or logical router loops down to the remote stable distribution branches, utilize the following decoupled staging architecture commands:

```bash
# Verify modified and untracked telemetry files
git status

# Stage assets safely 
git add src/static/index.html

# Commit changes locally using strict semantic categorization tags
git commit -m "feat: enhance light theme text color contrast configurations"

# Deploy stable distribution upstream
git push origin main

```
## 👨‍💻 Author
Bharath Raj
GitHub: https://github.com/Bharathrajzero

---

## 📝 License

This project is licensed under the MIT License © 2026 Bharath Raj, AlphaGroup Ltd.
