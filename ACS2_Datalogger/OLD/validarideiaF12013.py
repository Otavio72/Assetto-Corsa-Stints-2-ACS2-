import socket
import struct
import os

# ==========================================
# 🗄️ BANCO DE DADOS (O CÉREBRO DO ACS 2)
# ==========================================

# DNA das pistas (Tamanho / Pico)
MAPA_PISTAS = {
    5301.926868: "AUSTRALIA"
}

# Posições dos boxes organizados por pista
MAPA_BOXES = {
    "AUSTRALIA": {
5129.36133: 'redbull1',
5121.79102: 'redbull2',
5144.31494: 'ferrari1',
5136.74707: 'ferrari2',
5157.30762: 'mclaren1',
5149.73779: 'mclaren2',
5170.30664: 'lotus1',
5162.73682: 'lotus2',
5185.24609: 'mercedez1',
5177.67676: 'mercedez2',
5198.24365: 'sauber1',
5190.67529: 'sauber2',
5211.25000: 'force1',
5203.68164: 'force2',
5226.18213: 'wilians1',
5218.61182: 'wilians2',
5239.17676: 'tororosso1',
5231.60693: 'tororosso2',
5252.18799: 'cartheran1',
5244.61865: 'cartheran2',
5267.1377: 'marrusia1',
5259.56738: 'marrusia2',
    }
}

# ==========================================
# ⚙️ LÓGICA DO PROGRAMA
# ==========================================

UDP_IP = "0.0.0.0"
UDP_PORT = 20777
INDICE_ALVO = 2

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def buscar_carro(pista, valor_box):
    # Procura o carro com uma margem de erro de 0.5 (meio metro)
    boxes = MAPA_BOXES.get(pista, {})
    for coord, nome in boxes.items():
        if abs(coord - valor_box) < 0.5:
            return nome
    return "Carro Desconhecido"

# Variáveis de Estado
valor_box_capturado = None
pico_atual = 0.0
pista_confirmada = None

limpar_tela()
print("=== 🛰️ ACS 2: INICIADO ===")
print("Aguardando você entrar no jogo e ficar no box...\n")

try:
    while True:
        data, addr = sock.recvfrom(2048)
        pacote = struct.unpack('f' * (len(data) // 4), data)
        valor_atual = pacote[INDICE_ALVO]

        # 1. CAPTURA INICIAL (QUANDO O CARRO ESTÁ NO BOX)
        if valor_atual > 0 and valor_box_capturado is None:
            valor_box_capturado = valor_atual
            print(f"🔒 [PASSO 1] Posição no Box capturada: {valor_box_capturado:.4f}")
            print("⏳ [PASSO 2] Saia do box e acelere para identificarmos a pista...")

        # 2. MONITORAMENTO DE PICO
        if valor_atual > pico_atual:
            pico_atual = valor_atual

            # 3. VERIFICAÇÃO DO DNA DA PISTA (Se ainda não confirmou)
            if pista_confirmada is None:
                for dna, nome_pista in MAPA_PISTAS.items():
                    # Se o pico chegar muito perto do DNA da pista (margem de 2.0 metros pra garantir)
                    if abs(pico_atual - dna) < 2.0:
                        pista_confirmada = nome_pista
                        
                        # 4. O BINGO! CRUZANDO OS DADOS
                        carro_identificado = buscar_carro(pista_confirmada, valor_box_capturado)
                        
                        print("\n" + "="*50)
                        print("🎉 BINGO! IDENTIFICAÇÃO CONCLUÍDA 🎉")
                        print("="*50)
                        print(f"📍 PISTA:  {pista_confirmada}")
                        print(f"🏎️ CARRO:  {carro_identificado} (Box original: {valor_box_capturado:.4f})")
                        print("="*50)
                        print("\nO programa agora sabe quem você é. Pode correr em paz! 🏁")

except KeyboardInterrupt:
    print("\n🛑 ACS 2 Encerrado.")