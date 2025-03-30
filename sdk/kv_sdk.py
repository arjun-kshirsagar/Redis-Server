import socket
import struct

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

# Example usage:
if __name__ == "__main__":
    client = KVClient()
    print("PUT foo=bar:", client.put("foo", "bar"))
    print("GET foo:", client.get("foo"))
    print("GET missing:", client.get("missing_key"))