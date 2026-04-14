import socket
import struct

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 20777))

last = None

while True:
    data, _ = sock.recvfrom(4096)
    values = struct.unpack('<38f', data)

    if last:
        changes = [abs(v - last[i]) for i, v in enumerate(values)]

        for i, c in enumerate(changes):
            if c > 0.5:
                print(f"[{i}] mudou muito: {values[i]}")

    last = values