# How to use the SDK?
1. Save the SDK(kv_sdk.py) file in your test directory.
2. Import the SDK in your main application / python interactive shell:
```python
from kv_sdk import KVClient
```
3. Initialize the client :
```python
client = KVClient(host="localhost", port=7171)
```
4. Use the client to interact with the server:
```python
# Store a key-value pair
client.put("key", "value")

# Retrieve a value by key
value = client.get("key")
print(value)
```