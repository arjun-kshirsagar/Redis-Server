from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, constr
from cachetools import LRUCache
import uvicorn
import os

class CacheService:
    def __init__(self, max_size=None):
        # Use environment variable or default to 10000
        max_size = max_size or int(os.getenv('MAX_CACHE_SIZE', 0.7 * 2 * 1024 * 1024 * 1024))
        print(max_size)
        self._cache = LRUCache(maxsize=max_size)
    
    async def put(self, key: str, value: str):
        if len(key) > 256 or len(value) > 256:
            raise ValueError("Key or value exceeds 256 characters")
        
        self._cache[key] = value
        return {"status": "OK",
            "key": key,
            "value": value
            }
    
    async def get(self, key: str):
        try:
            if key not in self._cache:
                response = {
                    "status": "ERROR",
                    "message": "Key not found."
                }
                return response
                # raise HTTPException(status_code=404, detail="Key not found")
            return {"value": self._cache[key]}
        except Exception as e:
            raise e

app = FastAPI()
cache_service = CacheService()

class CacheEntry(BaseModel):
    key: constr(max_length=256)
    value: constr(max_length=256)

@app.post("/put")
async def put_key(entry: CacheEntry):
    return await cache_service.put(entry.key, entry.value)

@app.get("/get")
async def get_key(key: str):
    return await cache_service.get(key)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7171)