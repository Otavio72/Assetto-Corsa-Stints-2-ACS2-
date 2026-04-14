import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 20777))

while True:
    data, _ = sock.recvfrom(4096)

    print("\nBYTES:", len(data))
    print("RAW:", data[:32])