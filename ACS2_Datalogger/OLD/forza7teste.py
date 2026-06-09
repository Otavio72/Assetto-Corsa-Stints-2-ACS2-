import socket
import struct
import matplotlib.pyplot as plt

# Usando a porta 5300 que você configurou no Forza
UDP_IP = "0.0.0.0"
UDP_PORT = 5300 

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

lista_x = []
lista_z = []

print("🛰️  MAPEADOR ATIVADO COM OFFSETS DO GITHUB (232 / 240)")
print("🏎️  Dê uma volta e aperte CTRL+C para ver o gráfico!")

try:
    while True:
        data, addr = sock.recvfrom(1024)
        
        # Se o pacote for muito curto, ignora
        if len(data) < 244:
            continue

        # Lendo os offsets exatos que você encontrou:
        # PositionX = 232 | PositionZ = 240
        px = struct.unpack('<f', data[232:236])[0]
        pz = struct.unpack('<f', data[240:244])[0]
        
        # Só armazena se o carro estiver no mapa (X e Z não zerados)
        if px != 0.0:
            # Filtro de movimento (só salva se mover > 0.5m) para o gráfico ficar limpo
            if not lista_x or (abs(px - lista_x[-1]) > 0.5 or abs(pz - lista_z[-1]) > 0.5):
                lista_x.append(px)
                lista_z.append(pz)
                print(f"\rPontos: {len(lista_x)} | X: {px:.2f} | Z: {pz:.2f}", end="")

except KeyboardInterrupt:
    print("\n\n🏁 Gerando traçado...")
    if len(lista_x) > 20:
        plt.figure(figsize=(10, 10))
        plt.plot(lista_x, lista_z, 'b-', linewidth=2, label='Traçado Real')
        plt.scatter(lista_x[0], lista_z[0], color='green', label='Início') # Ponto de largada
        
        plt.title("Mapa da Pista - Forza 7 (GitHub Offsets)")
        plt.axis('equal') # Mantém a escala real da pista
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.show()
    else:
        print("❌ Dados insuficientes. O carro andou?")