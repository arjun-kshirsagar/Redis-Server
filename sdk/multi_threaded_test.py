
import random
import string
import socket
import struct
import time
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

class KVClient:
    CMD_PUT = 1
    CMD_GET = 2
    STATUS_OK = 1
    STATUS_ERROR = 2

    def __init__(self, host='127.0.0.1', port=7171):
        self.host = host
        self.port = port

    def put(self, key: str, value: str) -> bool:
        key_b = key.encode('utf-8')
        val_b = value.encode('utf-8')
        payload = (
            bytes([self.CMD_PUT]) +
            struct.pack(">H", len(key_b)) +
            struct.pack(">H", len(val_b)) +
            key_b +
            val_b
        )
        with socket.create_connection((self.host, self.port)) as s:
            s.sendall(payload)
            resp = s.recv(1024)
            return self._parse_status(resp)

    def get(self, key: str) -> str:
        key_b = key.encode('utf-8')
        payload = (
            bytes([self.CMD_GET]) +
            struct.pack(">H", len(key_b)) +
            key_b
        )
        with socket.create_connection((self.host, self.port)) as s:
            s.sendall(payload)
            resp = s.recv(1024)
            status, val = self._parse_response(resp)
            if status == self.STATUS_OK:
                return val
            else:
                raise Exception(f"Error from server: {val}")

    def _parse_status(self, resp: bytes) -> bool:
        if not resp:
            return False
        status = resp[0]
        return status == self.STATUS_OK

    def _parse_response(self, resp: bytes):
        if not resp or len(resp) < 3:
            return None, "No response or malformed response"
        status = resp[0]
        length = struct.unpack(">H", resp[1:3])[0]
        value = resp[3:3+length].decode('utf-8')
        return status, value

# Shared resources
key_store = {}
lock = Lock()

def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def store_key_value(key, value):
    with lock:
        key_store[key] = value

def get_key_value(key):
    with lock:
        return key_store.get(key)

def get_random_key():
    with lock:
        if key_store:
            return random.choice(list(key_store.keys()))
        return None

def main_thread(thread_id):
    client = KVClient()

    total_requests = 0
    failed_requests = 0
    start_time = time.time()

    for _ in range(1000):  # Each thread does 1000 requests
        action = random.choices(["put", "get"], weights=[0.4, 0.6])[0]

        if action == "put":
            key = generate_random_string()
            value = generate_random_string()
            success = client.put(key, value)
            print(success)
            total_requests += 1
            if not success:
                failed_requests += 1
                print(f"[Thread {thread_id}] Failed to put key: {key}")
            else:
                store_key_value(key, value)
                print(f"[Thread {thread_id}] Put key: {key} with value: {value}")

        elif action == "get":
            key = get_random_key()
            if key is None:
                key = generate_random_string()

            try:
                response_value = client.get(key)
                total_requests += 1
                expected_value = get_key_value(key)

                if expected_value and response_value == expected_value:
                    print(f"[Thread {thread_id}] Retrieved correct value for key: {key}")
                else:
                    print(f"[Thread {thread_id}] Value mismatch for key: {key}. Expected: {expected_value}, Got: {response_value}")
            except Exception as e:
                failed_requests += 1
                print(f"[Thread {thread_id}] Exception for GET {key}: {e}")

    total_time = time.time() - start_time
    print(f"\n[Thread {thread_id}] Completed {total_requests} requests in {total_time:.2f}s")
    print(f"[Thread {thread_id}] Failed requests: {failed_requests}")
    print(f"[Thread {thread_id}] RPS: {total_requests / total_time:.2f}")

def run_threads(thread_count=10):
    start = time.time()
    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        executor.map(main_thread, range(thread_count))
    print(f"RPS: {thread_count * 1000 / (time.time() - start):.2f}")

if __name__ == "__main__":
    run_threads(thread_count=10)  # You can change the number of threads here
