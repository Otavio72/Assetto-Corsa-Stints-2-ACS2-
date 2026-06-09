import socket
import struct
import os
import msvcrt

# Configurações
UDP_IP = "0.0.0.0"
UDP_PORT = 20777
INDICE_ALVO = 2

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def limpar_buffer_socket(s):
    s.setblocking(0)
    try:
        while True: s.recvfrom(2048)
    except BlockingIOError: pass
    s.setblocking(1)

pista_nome = input("📍 Qual o nome da pista? ").strip()
filename = f"boxes_{pista_nome.lower()}.txt"

# Cria o arquivo e coloca o cabeçalho
with open(filename, "w") as f:
    f.write(f"--- DADOS DE BOX: {pista_nome.upper()} ---\n")

limpar_tela()
print(f"=== 🛠️ ACS 2: MAPEADOR INSTANTÂNEO ({pista_nome.upper()}) ===")
print(f"💾 Os dados serão gravados direto em: {filename}")
print("1. ENTER para congelar | 2. 's' para confirmar | 3. Digite o nome\n")

try:
    limpar_buffer_socket(sock)
    count = 0
    
    while True:
        data, addr = sock.recvfrom(2048)
        pacote = struct.unpack('f' * (len(data) // 4), data)
        valor_atual = round(pacote[INDICE_ALVO], 5)

        print(f"\r📡 LENDO... Valor: {valor_atual:.5f} | Salvos: {count}", end="")

        if msvcrt.kbhit():
            if msvcrt.getch() == b'\r': 
                print(f"\n\n🛑 [CONGELADO]: {valor_atual:.5f}")
                confirma = input("👉 Confirmar? (s/n): ").strip().lower()
                
                if confirma == 's':
                    nome = input("🏷️ Piloto (ou 'SAIR'): ").strip()
                    if nome.upper() == 'SAIR': break
                    
                    # SALVAMENTO INSTANTÂNEO AQUI:
                    with open(filename, "a") as f: # "a" de append (adicionar)
                        f.write(f"{valor_atual}: '{nome}',\n")
                    
                    count += 1
                    print(f"✅ GRAVADO NO ARQUIVO!")
                else:
                    print("❌ Descartado!")
                
                print("-" * 30)
                limpar_buffer_socket(sock)

except KeyboardInterrupt:
    print(f"\n\nInterrompido! O que foi salvo até agora está em {filename}")

print(f"\n🏁 Processo finalizado. Verifique o arquivo {filename} na pasta do script!")