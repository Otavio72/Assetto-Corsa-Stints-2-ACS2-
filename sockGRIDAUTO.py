import socket
import struct

# Configuração do socket
UDP_IP = "127.0.0.1"
UDP_PORT = 20777
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("🏎️ Aguardando Grid Autosport...")
ultima_volta = 0
ultimo_tempo_volta = 0
while True:
    data, addr = sock.recvfrom(2048) # O pacote costuma ter ~64 bytes no modo 3
    
    # Exemplo: Pegando a velocidade (que costuma ser o float na posição 7)
    # Você vai precisar do mapeamento completo da Codemasters
    telemetria = struct.unpack('f' * (len(data) // 4), data)
    velocidade_kmh = telemetria[7] * 3.6
    tempo_volta = telemetria[1]
    volta_numero = int(telemetria[3])

    #print(f"tempo_volta: {tempo_volta}")
    

    if volta_numero != ultima_volta:
        if volta_numero != -1:
            print(f"tempo_volta: {ultimo_tempo_volta} // volta_numero: {ultima_volta}")
        ultima_volta = volta_numero
    ultimo_tempo_volta = tempo_volta
        