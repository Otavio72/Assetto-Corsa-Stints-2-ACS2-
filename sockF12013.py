import socket
import struct
import time
import json
import os
# DNA das pistas (Tamanho / Pico)
#MAPA_PISTAS = {
 #   5301.926868: "AUSTRALIA"
#}

#MAPA_BOXES = {
 #   "AUSTRALIA": {
#5129.36133: 'redbull1',
#5121.79102: 'redbull2',
#5144.31494: 'ferrari1',
#5136.74707: 'ferrari2',
#5157.30762: 'mclaren1',
#5149.73779: 'mclaren2',
#5170.30664: 'lotus1',
#5162.73682: 'lotus2',
#5185.24609: 'mercedez1',
#5177.67676: 'mercedez2',
#5198.24365: 'sauber1',
#5190.67529: 'sauber2',
#35211.25000: 'force1',
#5203.68164: 'force2',
#5226.18213: 'wilians1',
#5218.61182: 'wilians2',
#5239.17676: 'tororosso1',
#5231.60693: 'tororosso2',
#5252.18799: 'cartheran1',
#5244.61865: 'cartheran2',
#5267.1377: 'marrusia1',
#5259.56738: 'marrusia2',
 #   }
#}

# Variáveis de Estado
valor_box_capturado = 0
pico_atual = 0.0
pista_confirmada = ""
ultima_volta = 0
ultima_volta_fechada = 0
contador_voltas = 0
ultimo_timer_sessao = -1
timer_pc = time.time()  # Relógio do PC guardando o início
contador_pacotes_iguais = 0


#def buscar_carro(pista, valor_box):
 #   # Procura o carro com uma margem de erro de 0.5 (meio metro)
  #  boxes = MAPA_BOXES.get(pista, {})
   # for coord, nome in boxes.items():
    #    if abs(coord - valor_box) < 0.5:
     #       return nome
    #return "Carro Desconhecido"


# =========================================================================
# 📂 DESCOBRIR PISTA
# =========================================================================

def descobrir_pista(pico_atual):

    caminho = "MapeamentosF12013/Pistas/pistas.txt"

    with open(caminho, "r", encoding="utf-8") as f:

        for linha in f:

            linha = linha.strip()

            if not linha:
                continue

            nome_pista, dna = linha.split()

            dna = float(dna)

            # margem de erro
            if abs(pico_atual - dna) < 2.0:

                return nome_pista

    return "PISTA_DESCONHECIDA"

# =========================================================================
# 🚗 DESCOBRIR CARRO
# =========================================================================

def buscar_carro(pista, valor_box):

    caminho = f"MapeamentosF12013/Carros/boxes_{pista.lower()}.txt"

    if not os.path.exists(caminho):
        return "Carro Desconhecido"

    with open(caminho, "r") as f:

        for linha in f:

            linha = linha.strip()

            # ignora linha vazia
            if not linha:
                continue

            try:

                # separa no :
                valor, nome = linha.split(":")

                # limpa valor
                #valor = float(valor.strip())
                valor = round(float(valor.strip()), 5)

                # limpa nome
                nome = nome.strip()
                nome = nome.replace("'", "")
                nome = nome.replace(",", "")

                # margem de erro
                if abs(valor - valor_box) < 0.5:

                    return nome

            except Exception as e:

                print(f"ERRO NA LINHA: {linha}")
                print(e)

    return "Carro Desconhecido"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 20777))
    
def PegarCarroEpista():
    global valor_box_capturado, pico_atual, pista_confirmada, ultimo_timer_sessao,contador_pacotes_iguais
    
    # 1. As variáveis de contagem PRECISAM estar fora do While
    count_val = 0
    v_antigo = 0.0

    #print("🛰️ Aguardando estabilização no Box...")
    print(
            '🛰️ Aguardando estabilização no Box...', end="",
            flush=True
        )

    try:
        while True:

            data, addr = sock.recvfrom(2048)

            pacote = struct.unpack(
                'f' * (len(data) // 4),
                data
            )

            #valor_atual = pacote[2]
            valor_atual = round(pacote[2], 5)

            # =========================================================
            # 📦 CAPTURAR BOX
            # =========================================================

            if valor_box_capturado == 0:

                if valor_atual > 0 and valor_atual == v_antigo:
                    count_val += 1
                else:
                    count_val = 0

                v_antigo = valor_atual

                if count_val >= 15:

                    valor_box_capturado = valor_atual

                    print(
                        f"\n✅ [BOX OK] Valor: {valor_box_capturado:.5f}",
                        flush=True
                    )

                else:

                    print(
                        f"\r⏳ Sincronizando: {count_val}/15",
                        end="",
                        flush=True
                    )

                    continue

            # =========================================================
            # 🏁 MONITORA PICO DA PISTA
            # =========================================================

            if valor_atual > pico_atual:
                pico_atual = valor_atual

            # =========================================================
            # 🌍 IDENTIFICA PISTA
            # =========================================================

            if valor_atual < pico_atual and pista_confirmada == "":

                pista = descobrir_pista(pico_atual)

                if pista != "PISTA_DESCONHECIDA":

                    pista_confirmada = pista

                    print(
                        f"\n🌍 [PISTA OK] Identificada: {pista_confirmada}",
                        flush=True
                    )

                    # =========================================================
                    # 🚗 IDENTIFICA CARRO
                    # =========================================================

                    carro_nome = buscar_carro(
                        pista_confirmada,
                        valor_box_capturado
                    )

                    print(
                        f"🏎️ [CARRO OK] Identificado: {carro_nome}",
                        flush=True
                    )

                    # =========================================================
                    # 🚀 INICIA TELEMETRIA
                    # =========================================================

                    SocketF12013(
                        sock,
                        contador_voltas,
                        carro_nome,
                        pista_confirmada,
                        ultima_volta
                    )

    except KeyboardInterrupt:

        print("\n🛑 Encerrado.")

def SocketF12013(sock,contador_voltas,carro_nome,pista_confirmada,ultima_volta):
    sock.settimeout(5)
    while True:
        try:
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

                print(
                    json.dumps(DataF12013),
                    flush=True
                    )

            ultima_volta = tempo_lap

        except socket.timeout:
            # 🚨 O ALARME TOCOU! Se passaram 5 segundos de silêncio absoluto no rádio
            print("\n🛑 [ACS 2] F1 2013 parou de enviar pacotes (Jogo pausado, no menu ou fechado).")
            print("FECHOU")
            sock.close() # Fecha a conexão limpa
            break # 🎯 Quebra o loop e encerra o stint com sucesso!
            
        except Exception as e:
            print(f"Erro inesperado: {e}")
            sock.close()
            break

            
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