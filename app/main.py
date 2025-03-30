import asyncio
import struct
from cachetools import LRUCache

# Protocol Constants
CMD_PUT    = 1
CMD_GET    = 2
STATUS_OK  = 1
STATUS_ERROR = 2
MAX_LENGTH = 256

# Global LRU cache instance. Adjust maxsize as needed.
cache = LRUCache(maxsize=2000000) # 2 * 1024 * 1024
# Use an asyncio lock to guard cache modifications for safe concurrent access.
cache_lock = asyncio.Lock()

async def handle_connection(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    addr = writer.get_extra_info('peername')
    try:
        while True:
            # Expect a single command byte
            cmd_data = await reader.readexactly(1)
            if not cmd_data:

                break

            cmd_type = cmd_data[0]

            if cmd_type == CMD_PUT:
                await handle_put(reader, writer)
            elif cmd_type == CMD_GET:
                await handle_get(reader, writer)
            else:
                await write_error_response(writer, "Unknown command")
    except asyncio.IncompleteReadError:
        # Connection closed by client
        pass
    except Exception as e:
        await write_error_response(writer, f"Server error: {e}")
    finally:
        writer.close()
        await writer.wait_closed()

async def handle_put(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    try:
        # Read key length (2 bytes) and value length (2 bytes)
        key_len_bytes = await reader.readexactly(2)
        value_len_bytes = await reader.readexactly(2)
        key_len = struct.unpack(">H", key_len_bytes)[0]
        value_len = struct.unpack(">H", value_len_bytes)[0]

        print(f"Key length: {key_len}, Value length: {value_len}")

        if key_len > MAX_LENGTH or value_len > MAX_LENGTH:
            await write_error_response(writer, "Key or value too long")
            return

        key_bytes = await reader.readexactly(key_len)
        value_bytes = await reader.readexactly(value_len)
        key = key_bytes.decode('utf-8')
        value = value_bytes.decode('utf-8')

        # Safely update the global LRU cache
        async with cache_lock:
            cache[key] = value

        writer.write(bytes([STATUS_OK]))
        await writer.drain()
    except Exception as e:
        await write_error_response(writer, f"PUT Error: {e}")

async def handle_get(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    try:
        # Read key length (2 bytes)
        key_len_bytes = await reader.readexactly(2)
        key_len = struct.unpack(">H", key_len_bytes)[0]

        if key_len > MAX_LENGTH:
            await write_error_response(writer, "Key too long")
            return

        key_bytes = await reader.readexactly(key_len)
        key = key_bytes.decode('utf-8')

        # Retrieve key from cache with lock
        async with cache_lock:
            value = cache.get(key, None)

        # If key does not exist, set value as "-1"
        if value is None:
            value = "Key not found"
        value_bytes = value.encode('utf-8')

        # Build the response: status byte, 2-byte length of value, then value
        response = bytes([STATUS_OK]) + struct.pack(">H", len(value_bytes)) + value_bytes
        writer.write(response)
        await writer.drain()
    except Exception as e:
        await write_error_response(writer, f"GET Error: {e}")

async def write_error_response(writer: asyncio.StreamWriter, message: str):
    message_bytes = message.encode('utf-8')
    response = bytes([STATUS_ERROR]) + struct.pack(">H", len(message_bytes)) + message_bytes
    writer.write(response)
    await writer.drain()

async def main():
    server = await asyncio.start_server(handle_connection, '0.0.0.0', 7171)
    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)

    print("🚀 Server is starting up!")
    print(f"TCP server is running on {addrs}")

    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())
