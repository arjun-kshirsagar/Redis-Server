Sure! Here's a sample README for your FastAPI-based key-value server:

---

# Key-Value Cache Server

This is a simple key-value server built using **FastAPI** and **Cachetools**. It provides a basic caching mechanism that allows you to store and retrieve key-value pairs with an optional in-memory cache backed by an LRU (Least Recently Used) cache.

## Features

- **Put Key-Value Pair**: Store key-value pairs.
- **Get Value by Key**: Retrieve values by providing the corresponding key.
- **Health Check**: Check if the server is running and healthy.
- **Custom Cache Size**: Cache size is configurable via an environment variable (`MAX_CACHE_SIZE`).

## Prerequisites

Ensure you have Python 3.7 or higher installed. The following Python packages are required:

- FastAPI
- pydantic
- cachetools
- uvicorn

## Installation

1. Clone this repository to your local machine:

```bash
git clone https://github.com/arjun-kshirsagar/redis-server.git
cd redis-server
```

2. Pull the docker image & run the container
```bash
docker pull arjunkshirsagar/key-value-server
```

## Running the Server

### Method 1
1. Pull the docker image
```bash
docker pull arjunkshirsagar/key-value-server 
```

2. Run the container
```bash
docker run -p 7171:7171 arjunkshirsagar/key-value-server
```

### Method 2

To run the server, execute the following command:

```bash
docker compose up
```

This will start the server at `http://127.0.0.1:7171`.

If you want to set a custom cache size, you can use the `MAX_CACHE_SIZE` environment variable (in bytes):

```bash
export MAX_CACHE_SIZE=10485760  # Example: 10MB
```

By default, the cache size is set to `70%` of 2GB (`0.7 * 2 * 1024 * 1024 * 1024`).

## API Endpoints

### 1. **PUT `/put`**
Store a key-value pair in the cache.

#### Request Body:
```json
{
  "key": "your_key",
  "value": "your_value"
}
```

#### Response:
```json
{
  "status": "OK",
  "key": "your_key",
  "value": "your_value"
}
```

#### Example cURL request:
```bash
curl -X 'POST' \
  'http://127.0.0.1:7171/put' \
  -H 'Content-Type: application/json' \
  -d '{
  "key": "name",
  "value": "John"
}'
```

### 2. **GET `/get`**
Retrieve the value for a given key.

#### Request Parameters:
- `key`: The key whose value you want to retrieve.

#### Response:
```json
{
  "value": "your_value"
}
```

If the key doesn't exist, the response will be:

```json
{
  "status": "ERROR",
  "message": "Key not found."
}
```

#### Example cURL request:
```bash
curl -X 'GET' 'http://127.0.0.1:7171/get?key=name'
```

### 3. **GET `/health`**
Check the health status of the server.

#### Response:
```json
{
  "status": "healthy"
}
```

#### Example cURL request:
```bash
curl -X 'GET' 'http://127.0.0.1:7171/health'
```

## Error Handling

- **404 - Key Not Found**: When trying to retrieve a key that doesn't exist in the cache.
- **400 - Invalid Key/Value**: If the key or value exceeds the allowed length (256 characters).

