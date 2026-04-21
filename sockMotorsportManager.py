import os
import csv
import shutil
import time

# --- CONFIGURAÇÃO ---
caminho_jogo = r"C:\Games\Motorsport Manager"
caminho_projeto = r"./logs_capturados" # Pasta onde você vai guardar os arquivos
timeout_maximo = 0  # Segundos que ele vai esperar antes de fechar


# Cria a pasta de destino se ela não existir
if not os.path.exists(caminho_projeto):
    os.makedirs(caminho_projeto)

print("🏎️  Bot de Captura ACS 2: Ativado!")
print("Aguardando arquivos .csv aparecerem...")

# Mapeamento fixo (Exemplo: você descobriu que a coluna 0 é Tempo e a 4 é Combustível)
MAPA_COLUNAS = {
    4: "Driver name1",
    5: "Driver Team1",
    6: "Lap Number1",
    37: "Fastest Lap1",
    38: "Fastest S11",
    39: "Fastest S21",
    40: "Fastest S31",

    46: "Driver name2",
    47: "Driver Team2",
    48: "Lap Number2",
    79: "Fastest Lap2",
    80: "Fastest S12",
    81: "Fastest S22",
    82: "Fastest S32",
}

while True:
    # Lista todos os arquivos .csv na pasta do jogo
    arquivos = [f for f in os.listdir(caminho_jogo) if f.endswith(".csv")]
    arquivoRecebido = [f for f in os.listdir(caminho_projeto) if f.endswith(".csv")]

    arquivos = [f for f in os.listdir(caminho_jogo) if f.endswith(".csv")]
    
    if not arquivos:
            timeout_maximo = timeout_maximo + 1
            time.sleep(1)
            
            if timeout_maximo <= 20:
                print(f"⏳ Nada encontrado... Desligando em {timeout_maximo}/{20}s", end="\r")
            else:
                print("\nFECHADO\n")
                break

    else:
            for arquivo in arquivos:     
                timeout_maximo = 0   
                if arquivo == "PitstopData.csv" or arquivo == "TyreInformationData.csv" or arquivo == "DriversTimingInformationData.csv":
                    caminho_completo = os.path.join(caminho_jogo, arquivo)
                    os.remove(caminho_completo)
                else:
                    origem = os.path.join(caminho_jogo, arquivo)
                        
                    # Criamos um nome com timestamp para não sobrescrever o anterior no seu projeto
                    novo_nome = f"{int(time.time())}_{arquivo}"
                    destino = os.path.join(caminho_projeto, novo_nome)
                    
                    try:
                        # O 'move' já tira da pasta do jogo e joga na sua
                        shutil.move(origem, destino)
                        #print(f"✅ Capturado: {arquivo} -> {novo_nome}")

                        arquivoProjeto = novo_nome
                        nome_original = arquivoProjeto
                        arquivoProjeto = arquivoProjeto.split("_")
                        caminho_leitura = os.path.join(caminho_projeto, nome_original)
                        if arquivoProjeto[1] == "TeamDriverInformationData.csv":

                                with open(destino, mode='r', encoding='utf-8') as f:
                                    # Lemos linha por linha como texto puro
                                    for linha_bruta in f:
                                        # 1. Limpamos a linha e dividimos pela vírgula
                                        # O strip() tira os espaços, o replace tira aspas
                                        colunas = [item.strip().replace('"', '') for item in linha_bruta.split(",")]

                                        # 2. Se a linha estiver vazia ou for curta demais, pula ela
                                        if len(colunas) < 10:
                                            continue

                                        dados_filtrados = {}
                                        
                                        # 3. Mapeamos as colunas usando os índices que você descobriu
                                        for indice, nome_da_coluna in MAPA_COLUNAS.items():
                                            try:
                                                # Agora 'colunas' é a nossa lista de dados limpos!
                                                valor = colunas[indice]
                                                dados_filtrados[nome_da_coluna] = valor
                                                print(dados_filtrados['Driver name1'])



                                            except IndexError:
                                                dados_filtrados[nome_da_coluna] = "N/A"

                                    





                    except PermissionError:
                        # Se o jogo estiver escrevendo, ele ignora e tenta no próximo segundo
                        pass
                    except Exception as e:
                        print(f"❌ Erro ao mover: {e}")

                # Checa a pasta a cada 1 segundo
                time.sleep(1)