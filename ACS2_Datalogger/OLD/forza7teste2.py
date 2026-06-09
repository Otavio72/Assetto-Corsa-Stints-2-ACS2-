import socket
import struct
import matplotlib.pyplot as plt

# Configuração
UDP_IP = "0.0.0.0"
UDP_PORT = 5300 

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

valores_linha = []
pontos_tempo = [] # Usaremos o contador de pacotes como "tempo" simplificado

print("📊 GERADOR DE ASSINATURA DE TRAÇADO")
print("🏎️  Percorra um setor da pista e aperte CTRL+C...")

try:
    contador = 0
    while True:
        data, addr = sock.recvfrom(1024)
        
        # Lendo o Byte 309 (NormalDrivingLine)
        line_val = struct.unpack('B', data[309:310])[0]
        
        # Armazenamos os dados
        valores_linha.append(line_val)
        pontos_tempo.append(contador)
        contador += 1
        
        if contador % 60 == 0:
            print(f"\rGravando assinatura... Pontos: {contador} | Valor Atual: {line_val}", end="")

except KeyboardInterrupt:
    print("\n\n🏁 Gerando gráfico de comportamento...")

    if len(valores_linha) > 10:
        plt.figure(figsize=(12, 5))
        
        # Desenha o comportamento da linha
        plt.plot(pontos_tempo, valores_linha, color='green', linewidth=1.5)
        
        # Estética
        plt.title("Assinatura Lateral da Pista (NormalDrivingLine)", fontsize=14)
        plt.xlabel("Tempo / Frames")
        plt.ylabel("Posição Lateral (0-255)")
        plt.grid(True, alpha=0.3)
        
        print("✅ Gráfico exibido! Observe as 'ondas' que representam as curvas.")
        plt.show()
    else:
        print("❌ Sem dados suficientes.")