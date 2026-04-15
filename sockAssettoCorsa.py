import socket
import struct


def processar_handshake(data):
    if len(data) != 408:
        print(f"⚠️ Pacote inesperado: {len(data)} bytes")
        return

    # Formato: 100 bytes string, 100 bytes string, int, int, 100 bytes string, 100 bytes string
    # '<' = Little Endian
    # '100s' = String de 100 bytes
    # 'i' = Inteiro de 4 bytes
    formato = '<100s100sii100s100s'
    
    unpacked = struct.unpack(formato, data)
    
    # Função interna para limpar o lixo do UTF-16
    def limpar(texto_bruto):
        return texto_bruto.decode('utf-16-le', errors='ignore').split('\x00')[0].strip()

    info = {
        "carro":  limpar(unpacked[0]),
        "piloto": limpar(unpacked[1]),
        "id":     unpacked[2],
        "ver":    unpacked[3],
        "pista":  limpar(unpacked[4]),
        "layout": limpar(unpacked[5])
    }
    
    print("\n🏎️  --- ASSETTO CORSA IDENTIFICADO ---")
    print(f"🚗 Carro:  {info['carro']}")
    print(f"👤 Piloto: {info['piloto']}")
    print(f"🏁 Pista:  {info['pista']} ({info['layout']})")
    print(f"⚙️  Versão: {info['ver']}")
    print("--------------------------------------\n")
    return info

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
data, addr = sock.recvfrom(1024)
packet = struct.pack('iii', 1, 1, 0)
print(f"✅ Recebido pacote de {len(data)} bytes de {addr}")
processar_handshake(data)

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
    # 👇 HANDSHAKE RESPONSE
    base = 8
    try:
        data, addr = sock.recvfrom(4096)
        size = len(data)
        unpacked = struct.unpack('<50s50sii50s50s', data[:208])

        speed_kmh = struct.unpack_from('<f', data, 8)[0]
        lapTime  = struct.unpack_from('<i', data, base + 32)[0]
        lastLap  = struct.unpack_from('<i', data, base + 36)[0]
        bestLap  = struct.unpack_from('<i', data, base + 40)[0]
        lapCount = struct.unpack_from('<i', data, base + 44)[0]


        print(f"KMH: {speed_kmh:.1f}, laptime {lapTime} lapcount {lapCount}")

    except struct.error as e:
            print("Erro ao decodificar handshake:", e)