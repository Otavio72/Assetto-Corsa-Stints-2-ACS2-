import os
import shutil
import time
import json

# --- CONFIGURAÇÃO ---
caminho_jogo = r"C:\Games\Motorsport Manager"
caminho_projeto = r"./logs_capturados"

timeout_maximo = 0
ultima_volta = 0
volta_atual = -1

dados_gerais = {}
dados_timing = {}
dados_pneus = {}
ultimas_voltas = {}

piloto1 = ""
piloto2 = ""

# Cria pasta se não existir
os.makedirs(caminho_projeto, exist_ok=True)

print(
    json.dumps({
        "TYPE": "STATUS",
        "CODE": "01",
        "MSG": "SockMotorsportManager iniciado"
    }),
    flush=True
)

# --- MAPAS ---
TeamDriverMAPA = {
    4: "Driver name1",
    5: "Driver Team1",
    6: "Lap Number1",
    37: "Fastest Lap1",
    46: "Driver name2",
    47: "Driver Team2",
    48: "Lap Number2",
    79: "Fastest Lap2",
}


#DriversTimingMAPA = {
 #   8: "Last Lap Time",
#}

TrackSessionMAPA = {
    4: "Circuit Name",
}

# --- LOOP PRINCIPAL ---
while True:
    arquivos = [f for f in os.listdir(caminho_jogo) if f.endswith(".csv")]

    #if not arquivos:
     #   timeout_maximo += 1
      #  time.sleep(1)

        #if timeout_maximo <= 1200:
         #   #print(f"⏳ Nada encontrado... {timeout_maximo}/1200s", end="\r")
          #  print(
           #         f"⏳ Nada encontrado... {timeout_maximo}/1200s", end="\r",
            #3        flush=True
             #   )
       # else:
        #    # Listamos tudo o que existe dentro do diretório
         #   for item in os.listdir(caminho_projeto):
          #      item_completo = os.path.join(caminho_projeto, item)
           #     try:
            #        if os.path.isfile(item_completo) or os.path.islink(item_completo):
             #           os.unlink(item_completo)  # Apaga arquivo ou link simbólico
              #      elif os.path.isdir(item_completo):
               #         shutil.rmtree(item_completo) # Apaga subpasta e tudo dentro dela
                #except Exception as e:
                    #print(f"❌ Erro ao apagar {item}: {e}")
                 #   print(
                  #          f"❌ Erro ao apagar {item}: {e}",
                   #         flush=True
                    #    )

            #print("✨ Pasta limpa! Encerrando...")
            #print(
             #   "✨ Pasta limpa! Encerrando...",
              #  flush=True
               # )
            #break
        #continue

    
    #timeout_maximo = 0

    for arquivo in arquivos:
        origem = os.path.join(caminho_jogo, arquivo)

        # ignora lixo
        if arquivo == "PitstopData.csv":
            try:
                os.remove(origem)
            except:
                pass
            continue

        novo_nome = f"{int(time.time())}_{arquivo}"
        destino = os.path.join(caminho_projeto, novo_nome)

        try:
            shutil.move(origem, destino)

            # -------- TEAM DRIVER --------
            if arquivo.endswith("TeamDriverInformationData.csv"):
                with open(destino, "r", encoding="utf-8") as f:
                    next(f)

                    for linha in f:
                        colunas = [c.strip().replace('"', '') for c in linha.split(",")]

                        if len(colunas) < 10:
                            continue

                        for idx, nome in TeamDriverMAPA.items():
                            dados_gerais[nome] = colunas[idx] if idx < len(colunas) else "N/A"

                        piloto1 = dados_gerais.get("Driver name1", "")
                        piloto2 = dados_gerais.get("Driver name2", "")

                        try:
                            volta_atual = int(dados_gerais.get("Lap Number1", "-1"))
                        except:
                            volta_atual = -1

                    # -------- TIMING --------
            elif arquivo.endswith("DriversTimingInformationData.csv"):
                with open(destino, "r", encoding="utf-8") as f:
                    next(f)

                    for linha in f:
                        colunas = [c.strip().replace('"', '') for c in linha.split(",")]

                        if len(colunas) < 10:
                            continue

                        # percorre a linha inteira procurando os pilotos
                        for i, valor in enumerate(colunas):

                            if valor == piloto1 or valor == piloto2:
                                nome_piloto = valor
                                timing_temp = {}

                                try:
                                    # 👇 PULO DO GATO
                                    # baseado no teu teste: last lap fica ~11 colunas depois
                                    indice_last_lap = i + 11

                                    last_lap = colunas[indice_last_lap]
                                    timing_temp["Last Lap Time"] = last_lap
                                    

                                except IndexError:
                                    timing_temp["Last Lap Time"] = "N/A"

                                # salva separado por piloto
                                dados_timing[nome_piloto] = timing_temp

                                #print(f"⏱️ {nome_piloto} | Last Lap: {timing_temp['Last Lap Time']}")
            # -------- TRACK SESSION --------
            elif arquivo.endswith("TrackSessionData.csv"):
                with open(destino, "r", encoding="utf-8") as f:
                    next(f)

                    for linha in f:
                        colunas = [c.strip().replace('"', '') for c in linha.split(",")]

                        if len(colunas) < 6:
                            continue

                        for idx, nome in TrackSessionMAPA.items():
                            dados_pneus[nome] = colunas[idx] if idx < len(colunas) else "N/A"

            try:
                    lap1 = int(dados_gerais.get('Lap Number1', -1))
                    lap2 = int(dados_gerais.get('Lap Number2', -1))
            except:
                    lap1 = lap2 = -1

                # PILOTO 1
            if piloto1 and lap1 > ultimas_voltas.get(piloto1, -1):
                    try:
                        tempo = float(dados_timing.get(piloto1, {}).get('Last Lap Time', -1))
                        pista = dados_pneus.get("Circuit Name", "Desconhecida")
                        
                    except:
                        tempo = -1

                    dataMMpiloto1 = {
                        "NomePiloto": dados_gerais['Driver name1'],
                        "Carro": dados_gerais['Driver Team1'],
                        "Volta": lap1,
                        "Tempo": tempo,
                        "Pista": pista
                    }

                    ultimas_voltas[piloto1] = lap1

        

                    print(
                            json.dumps(dataMMpiloto1),
                            flush=True
                            )
                    
                    print(
                        json.dumps({
                            "TYPE": "STATUS",
                            "CODE": "02",
                            "MSG": "Recebendo Dados PILOTO 1"
                        }),
                        flush=True
                    )

                    #print(
                     #   json.dumps({
                      #      "TYPE": "STATUS",
                       #     "CODE": "07",
                        #    "MSG": "Recebendo Dados PILOTO 1"
                        #}),
                        #flush=True
                    #)

                    

                # PILOTO 2
            if piloto2 and lap2 > ultimas_voltas.get(piloto2, -1):
                    try:
                        tempo = float(dados_timing.get(piloto2, {}).get('Last Lap Time', -1))
                        pista = dados_pneus.get("Circuit Name", "Desconhecida")
                    except:
                        tempo = -1

                    dataMMpiloto2 = {
                        "NomePiloto": dados_gerais['Driver name2'],
                        "NomeTime": dados_gerais['Driver Team2'],
                        "Volta": lap2,
                        "Tempo": tempo,
                        "Pista": pista
                    }

                    ultimas_voltas[piloto2] = lap2
                    
                    print(
                            json.dumps(dataMMpiloto2),
                            flush=True
                            )
                    
                    print(
                        json.dumps({
                            "TYPE": "STATUS",
                            "CODE": "02",
                            "MSG": "Recebendo Dados PILOTO 2"
                        }),
                        flush=True
                    )

                    #print(
                    #    json.dumps({
                     #       "TYPE": "STATUS",
                      #      "CODE": "07",
                       #     "MSG": "Recebendo Dados PILOTO 2"
                        #}),
                        #flush=True
                    #)
                
        except PermissionError:
            pass
        except Exception as e:
            #print(f"❌ Erro: {e}")
            print(
                json.dumps({
                    "TYPE": "STATUS",
                    "CODE": "00",
                    "MSG": f"Erro inesperado: {e}"
                    }),
                    flush=True
                    )



            

    # sleep FORA do loop de arquivos (importante)
    time.sleep(1)