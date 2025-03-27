from fastapi import FastAPI, HTTPException
from collections import OrderedDict
from typing import Dict
import asyncio

class LRUCache:
    def __init__(self, capacity: int = 10000):  # Adjust capacity as needed
        self.cache: OrderedDict[str, str] = OrderedDict()
        self.capacity = capacity
        self.lock = asyncio.Lock()
    
    async def get(self, key: str) -> str:
        async with self.lock:
            if key in self.cache:
                self.cache.move_to_end(key)  # Mark key as recently used
                return self.cache[key]
            raise HTTPException(status_code=404, detail="Key not found")
    
    async def put(self, key: str, value: str):
        async with self.lock:
            if key in self.cache:
                self.cache.move_to_end(key)
            self.cache[key] = value
            if len(self.cache) > self.capacity:
                self.cache.popitem(last=False)  # Remove least recently used item

app = FastAPI()
cache = LRUCache(capacity=5000)  # Can be tuned based on memory usage

@app.put("/put/{key}")
async def put_key_value(key: str, value: str):
    if len(key) > 256 or len(value) > 256:
        raise HTTPException(status_code=400, detail="Key or value exceeds length limit")
    await cache.put(key, value)
    return {"message": "Success"}

@app.get("/get/{key}")
async def get_key_value(key: str):
    return {"value": await cache.get(key)}
