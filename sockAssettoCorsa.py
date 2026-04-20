import socket
import struct
import time

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


    carro = limpar(unpacked[0])
    pista = limpar(unpacked[4])
    layout = limpar(unpacked[5])
    
    
    info = f"carro: {carro} pista: {pista} layout: {layout}"
    return info

def SocketAssettoCorsa(sock, info_sessao, UDP_IP, UDP_PORT):
# =========================
# 2. SUBSCRIBE (UPDATE)
# =========================
    subscribe = struct.pack('iii', 1, 1, 1)
    sock.sendto(subscribe, (UDP_IP, UDP_PORT))
    print("Subscribe enviado")

# =========================
# 3. RECEBER DADOS
# =========================
    ultima_volta = -1  # Começa em -1 para capturar a volta 0 assim que começar
    print("🚀 ACS 2: Monitorando Assetto Corsa... (Aguardando fechamento de volta)")

    while True:
        # 👇 HANDSHAKE RESPONSE
        base = 8
    
        try:
            data, addr = sock.recvfrom(4096)
            #size = len(data)
            #unpacked = struct.unpack('<50s50sii50s50s', data[:208])
            lapCount = struct.unpack_from('<i', data, base + 44)[0]
            
            if lapCount != ultima_volta:
                #speed_kmh = struct.unpack_from('<f', data, 8)[0]
                #lapTime  = struct.unpack_from('<i', data, base + 32)[0]
                lastLap  = struct.unpack_from('<i', data, base + 36)[0]
                bestLap  = struct.unpack_from('<i', data, base + 40)[0]
                
                ultima_volta = lapCount

                DadosAssettoCorsa = {
                "info_sessao": info_sessao,
                "lastLap": lastLap,
                "ultima_volta": ultima_volta,
                "bestLap": bestLap
                }

                print(DadosAssettoCorsa)

        except struct.error as e:
                print("Erro ao decodificar handshake:", e)

# --- CONFIGURAÇÃO INICIAL ---
UDP_IP = "127.0.0.1"
UDP_PORT = 9996

print("🔍 Aguardando Assetto Corsa... (Pode abrir o jogo agora!)")

while True:
    # Criamos o socket DENTRO do loop de espera para garantir que ele esteja limpo
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # O PULO DO GATO REFORÇADO 🐈
    if hasattr(socket, 'SIO_UDP_CONNRESET'):
        sock.ioctl(socket.SIO_UDP_CONNRESET, False)
    
    try:
        sock.settimeout(1.0) # Espera 1 seg por tentativa
        handshake = struct.pack('iii', 1, 1, 0)
        sock.sendto(handshake, (UDP_IP, UDP_PORT))
        
        data, addr = sock.recvfrom(1024)
        
        if len(data) == 408:
            info_sessao = processar_handshake(data)
            if info_sessao:
                SocketAssettoCorsa(sock, info_sessao, UDP_IP, UDP_PORT)
                
    except (socket.timeout, ConnectionResetError):
        # O ConnectionResetError é o WinError 10054
        # Se der esse erro, a gente só ignora e tenta de novo
        sock.close() # Fecha o socket atual pra abrir um novo na próxima volta
        time.sleep(1) # Espera um pouco pra não fritar o processador
        continue
    except KeyboardInterrupt:
        print("\nSaindo...")
        break

