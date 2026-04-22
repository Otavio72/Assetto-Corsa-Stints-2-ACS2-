import os
import shutil
import time

# --- CONFIGURAÇÃO ---
caminho_jogo = r"C:\Games\Motorsport Manager"
caminho_projeto = r"./logs_capturados"

timeout_maximo = 0
ultima_volta = 0
volta_atual = -1

dados_gerais = {}
dados_timing = {}
dados_pneus = {}

piloto1 = ""
piloto2 = ""

# Cria pasta se não existir
os.makedirs(caminho_projeto, exist_ok=True)

print("🏎️ Bot de Captura ACS 2: Ativado!")

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

    if not arquivos:
        timeout_maximo += 1
        time.sleep(1)

        if timeout_maximo <= 100:
            print(f"⏳ Nada encontrado... {timeout_maximo}/100s", end="\r")
        else:
            print("\n⛔ Encerrando...")
            break
        continue

    timeout_maximo = 0

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

            # DEBUG opcional
            #print(dados_gerais)
            #print(dados_timing)
            #print(dados_pneus)

            if ultima_volta != volta_atual:
                print(
                        f"{dados_gerais['Driver name1']} | "
                        f"{dados_gerais['Driver Team1']} | "
                        f"Lap: {dados_gerais['Lap Number1']} | "
                        f"{dados_timing.get(piloto1)}"
                    )
                
                print(
                        f"{dados_gerais['Driver name2']} | "
                        f"{dados_gerais['Driver Team2']} | "
                        f"Lap: {dados_gerais['Lap Number2']} | "
                        f"{dados_timing.get(piloto2)}"
                    )
                

                ultima_volta = volta_atual
            
            else:
                timeout_maximo = 100

        except PermissionError:
            pass
        except Exception as e:
            print(f"❌ Erro: {e}")

    # sleep FORA do loop de arquivos (importante)
    time.sleep(1)