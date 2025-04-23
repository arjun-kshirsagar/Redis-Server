# High-Throughput TCP Key-Value Cache Server

This project implements a **high-throughput, low-latency key-value cache server** using a custom **TCP protocol**. It's optimized for high-concurrency environments, making it ideal for use cases that demand speed, simplicity, and scale.

> **Note**: If you're looking for a traditional **HTTP-based key-value server**, check out the [`http-server`](https://github.com/arjun-kshirsagar/redis-server/tree/http-server) branch of this repository.

---

## 🚀 Features

- ⚡ **High-Throughput TCP Server**: Designed to efficiently handle thousands of concurrent TCP connections.
- 📦 **Key-Value Caching**: Supports `PUT` and `GET` operations with LRU eviction via `Cachetools`.
- 🧰 **Python SDK Included**: Quickly build or test clients using the provided SDK (`sdk/` directory).
- 🐳 **Docker Support**: Easily deploy with Docker or Docker Compose.

---

## 🧱 Prerequisites

- Python 3.7+ (for SDK or development)
- Docker (recommended for running the server)

---

## 📦 Installation

1. **Clone the repository**:

```bash
git clone https://github.com/arjun-kshirsagar/redis-server.git
cd redis-server
```

2. **Run using Docker**:

```bash
docker pull arjunkshirsagar/key-value-server
docker run -p 7171:7171 arjunkshirsagar/key-value-server
```

Or use Docker Compose:

```bash
docker compose up
```

> The TCP server will be available on `127.0.0.1:7171`.


---

## 🧪 Testing with SDK

We provide a Python SDK in the [`sdk/`](./sdk) directory to simplify testing and integration.

📄 **Refer to [`sdk.md`](./sdk/sdk.md)** for detailed usage instructions.

---

## 🗂 Branches

- **`main`**: ⚡ High-performance **TCP-based** key-value server (this branch).
- **[`http-server`](https://github.com/arjun-kshirsagar/redis-server/tree/http-server)**: 🌐 Traditional **HTTP-based** server built using FastAPI with REST endpoints.

---

## 📌 Notes

- Designed for **internal infrastructure**, **microservices**, or any system requiring fast cache lookups.
- Consider using **HTTP version** if you need REST APIs or client-friendly integrations.
