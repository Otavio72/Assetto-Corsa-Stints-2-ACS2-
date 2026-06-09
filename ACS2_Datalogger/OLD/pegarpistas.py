import socket
import struct
import os
import time

# Configurações
UDP_IP = "0.0.0.0"
UDP_PORT = 20777
INDICE_ALVO = 2  # Mude aqui se o tamanho da pista estiver em outro índice

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

pico_valor = 0.0
capturando = False

limpar_tela()
print("=== 🛰️ ACS 2: CAPTURADOR DE DNA (TAMANHO DA PISTA) ===")
print(f"Monitorando índice: [{INDICE_ALVO}]")
print("Aguardando telemetria... (Entre na pista ou carregue o circuito)")

try:
    while True:
        data, addr = sock.recvfrom(2048)
        pacote = struct.unpack('f' * (len(data) // 4), data)
        valor_atual = pacote[INDICE_ALVO]

        # Lógica de Captura
        if valor_atual > 0:
            capturando = True
            if valor_atual > pico_valor:
                pico_valor = valor_atual
            
            # Feedback em tempo real
            print(f"\r📡 Capturando... Valor atual: {valor_atual:.4f} | Pico: {pico_valor:.4f}", end="")
        
        # Se o valor zerar e estávamos capturando, significa que você saiu da pista
        elif valor_atual == 0 and capturando:
            print("\n\n" + "="*50)
            print("🏁 SESSÃO ENCERRADA / VALOR ZERADO")
            print(f"💎 DNA ENCONTRADO (MAIOR VALOR): {pico_valor:.4f}")
            print("="*50)
            
            # Reset para a próxima captura
            input("\nAperte ENTER para limpar e aguardar a próxima pista...")
            pico_valor = 0.0
            capturando = False
            limpar_tela()
            print("=== 🛰️ ACS 2: AGUARDANDO NOVA PISTA... ===")

except KeyboardInterrupt:
    print(f"\n\n🛑 Scanner parado. Último pico registrado: {pico_valor:.4f}")