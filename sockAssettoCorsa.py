import socket
import struct
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 9996

#SO E POSSIVEL PEGAR CARRO E PISTA VIA SHAREDMEMORY O PACOTE DE 208 BYTES DO ASSETTO CORSA NAO FUNCIONA

# cria socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# opcional: bind pra receber resposta
sock.bind(("0.0.0.0", 0))

# =========================
# 1. HANDSHAKE
# =========================
handshake = struct.pack('iii', 1, 1, 0)
sock.sendto(handshake, (UDP_IP, UDP_PORT))
print("Handshake enviado")

time.sleep(0.5)

# =========================
# 2. SUBSCRIBE (UPDATE)
# =========================
subscribe = struct.pack('iii', 1, 1, 1)
sock.sendto(subscribe, (UDP_IP, UDP_PORT))
print("Subscribe enviado")

# =========================
# 3. RECEBER DADOS
# =========================
while True:
    data, addr = sock.recvfrom(4096)
    size = len(data)
    #print(f"Recebido {len(data)} bytes de {addr}")
    #print(len(data))

    # 👇 HANDSHAKE RESPONSE
    if size == 208 and car is None:
        try:
            unpacked = struct.unpack('<50s50sii50s50s', data)

            car = unpacked[0].decode('latin-1').strip('\x00')
            driver = unpacked[1].decode('latin-1').strip('\x00')
            track = unpacked[4].decode('latin-1').strip('\x00')
            config = unpacked[5].decode('latin-1').strip('\x00')

            print("🎯 HANDSHAKE CAPTURADO")
            print(f"Carro: {car}")
            print(f"Pista: {track} ({config})")

        except Exception as e:
            print("Erro handshake:", e)

    base = 8
    try:
        unpacked = struct.unpack('<50s50sii50s50s', data[:208])

        speed_kmh = struct.unpack_from('<f', data, 8)[0]
        lapTime  = struct.unpack_from('<i', data, base + 32)[0]
        lastLap  = struct.unpack_from('<i', data, base + 36)[0]
        bestLap  = struct.unpack_from('<i', data, base + 40)[0]
        lapCount = struct.unpack_from('<i', data, base + 44)[0]


        print(f"KMH: {speed_kmh:.1f}, laptime {lapTime} lapcount {lapCount}")

    except struct.error as e:
            print("Erro ao decodificar handshake:", e)