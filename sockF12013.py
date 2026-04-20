import socket
import struct

# DNA das pistas (Tamanho / Pico)
MAPA_PISTAS = {
    5301.926868: "AUSTRALIA"
}

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

# Variáveis de Estado
valor_box_capturado = 0
pico_atual = 0.0
pista_confirmada = 0
ultima_volta = 0
ultima_volta_fechada = 0
contador_voltas = 0


def buscar_carro(pista, valor_box):
    # Procura o carro com uma margem de erro de 0.5 (meio metro)
    boxes = MAPA_BOXES.get(pista, {})
    for coord, nome in boxes.items():
        if abs(coord - valor_box) < 0.5:
            return nome
    return "Carro Desconhecido"


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 20777))
    
def PegarCarroEpista():
    global valor_box_capturado, pico_atual, pista_confirmada
    
    # 1. As variáveis de contagem PRECISAM estar fora do While
    count_val = 0
    v_antigo = 0.0

    print("🛰️ Aguardando estabilização no Box...")

    try:
        while True:
            data, addr = sock.recvfrom(2048)
            pacote = struct.unpack('f' * (len(data) // 4), data)
            valor_atual = pacote[2]

            # --- ETAPA A: CAPTURAR O BOX (SÓ RODA SE AINDA NÃO TEMOS O BOX) ---
            if valor_box_capturado == 0:
                if valor_atual > 0 and valor_atual == v_antigo:
                    count_val += 1
                else:
                    count_val = 0
                
                v_antigo = valor_atual # Atualiza para a próxima comparação

                if count_val >= 15: # Aumentei pra 15 pra garantir
                    valor_box_capturado = valor_atual
                    print(f"\n✅ [BOX OK] Valor: {valor_box_capturado:.4f}")
                else:
                    print(f"\r⏳ Sincronizando: {count_val}/15", end="")
                    continue # Volta pro topo para pegar o próximo pacote

            # --- ETAPA B: BUSCAR A PISTA (SÓ CHEGA AQUI SE O BOX JÁ FOI CAPTURADO) ---
            
            # Monitora o pico (distância percorrida)
            if valor_atual > pico_atual:
                pico_atual = valor_atual

            # Se ainda não sabemos a pista, tentamos identificar pelo DNA
            if pista_confirmada == 0:
                for dna, nome_pista in MAPA_PISTAS.items():
                    if abs(pico_atual - dna) < 2.0:
                        pista_confirmada = nome_pista
                        print(f"\n🌍 [PISTA OK] Identificada: {pista_confirmada}")
                        
                        # ETAPA C: BINGO!
                        carro_nome = buscar_carro(pista_confirmada, valor_box_capturado)
                        print(f"🏎️ [CARRO OK] Identificado: {carro_nome}")
                        
                        # Passa o bastão para a telemetria principal e encerra
                        SocketF12013(contador_voltas,carro_nome,pista_confirmada,ultima_volta,ultima_volta_fechada)
                        

    except KeyboardInterrupt:
        print("\n🛑 Encerrado.")

def SocketF12013(contador_voltas,carro_nome,pista_confirmada,ultima_volta,ultima_volta_fechada):
    while True:
        data, _ = sock.recvfrom(4096)
        pacote = struct.unpack('f' * (len(data) // 4), data)

        #velocidade: velocidade = pacote[7] * 3.6,
        # tempo de volta: volta = pacote[1]
        # ACELERADOR teste3 = pacote[29]
        # FREIO teste5 = pacote[31]
        # POSICAO NA CORRIDA teste1 = pacote[39]
        # quantidade de voltas da corrida teste1 = pacote[60]
        # --- Processamento dos dados ---
        #vel_kmh    = pacote[7] * 3.6
        tempo_lap  = pacote[1]
        #gas        = pacote[29] * 100  # Convertendo para 0-100%
        #brake      = pacote[31] * 100  # Convertendo para 0-100%
        #pos        = int(pacote[39])
        total_laps = int(pacote[60])

        if tempo_lap < ultima_volta and ultima_volta > 10.0:

            ultima_volta_fechada = ultima_volta

            contador_voltas += 1
            volta_atual = contador_voltas + 1
            voltas_restantes = total_laps - contador_voltas

            DataF12013 = {
                "Tempo": ultima_volta_fechada,
                "VoltaAtual": volta_atual,
                "Restantes": voltas_restantes,
                "Pista": pista_confirmada,
                "Carro": carro_nome
            }

            print(DataF12013)

        ultima_volta = tempo_lap

            
        # AGORA O PULO DO GATO: 
        # Antes de receber o próximo pacote, guardamos o tempo de AGORA 
        # para ele ser o 'ANTERIOR' na próxima comparação.


        # No seu print, você mostra a 'ultima_volta_fechada' (que está congelada)
        #print(f"\r🕒 ATUAL: {tempo_lap:6.2f}s | ÚLTIMA VOLTA: {ultima_volta_fechada:6.2f}s", end="")
        #f"pista_confirmada: {pista_confirmada} carro_identificado: {carro_identificado}  VOLTA: {ultima_volta}s | TOTAL: {total_laps:02d} "
        # --- Organização Visual ---
        # Criando barras visuais para os pedais (opcional, mas fica irado!)
        #bar_gas = "█" * int(gas / 10)
        #bar_brk = "█" * int(brake / 10)

        # O print formatado
        # \r no início faz ele voltar para o começo da linha
        #print(f" | GAS: [{bar_gas:<10}] | FRE: [{bar_brk:<10}]", end="\r")

if __name__ == "__main__":
    PegarCarroEpista()