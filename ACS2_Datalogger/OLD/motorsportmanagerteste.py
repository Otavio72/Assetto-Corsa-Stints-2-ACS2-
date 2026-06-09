import os
import csv
import json
import time
import shutil

# --- CONFIGURAÇÃO ---
PASTA_ENTRADA = r"./logs_capturados"
PASTA_PROCESSADOS = r"./processados"
PASTA_JSON = r"./json_outputs"
TIMEOUT_FINALIZACAO = 10  # Segundos de silêncio para considerar fim de corrida

# Garantir que as pastas existam
for pasta in [PASTA_PROCESSADOS, PASTA_JSON]:
    if not os.path.exists(pasta):
        os.makedirs(pasta)

def processar_arquivo_csv(nome_arquivo):
    caminho_in = os.path.join(PASTA_ENTRADA, nome_arquivo)
    dados_finais = []

    print(f"🛠️  Processando: {nome_arquivo}...")
    
    try:
        with open(caminho_in, mode='r', encoding='utf-8') as f:
            # Lemos a primeira linha para limpar o cabeçalho
            cabecalho_cru = f.readline()
            colunas_limpas = [c.strip().replace('"', '') for c in cabecalho_cru.split(",")]
            
            # Usamos o DictReader com o cabeçalho já limpo
            leitor = csv.DictReader(f, fieldnames=colunas_limpas)

            for linha in leitor:
                # Pegamos apenas o que interessa pelo NOME da coluna
                # O .strip() no valor limpa aqueles espaços extras do MM
                registro = {
                    "piloto": linha.get("Driver Name", "N/A").strip(),
                    "equipe": linha.get("Team", "N/A").strip(),
                    "volta":  linha.get("Lap Number", "0").strip(),
                    "s1":     linha.get("Fastest S1", "0").strip(),
                    "s2":     linha.get("Fastest S2", "0").strip(),
                    "s3":     linha.get("Fastest S3", "0").strip()
                }
                dados_finais.append(registro)

        # 1. Salva o JSON
        nome_json = nome_arquivo.replace(".csv", ".json")
        caminho_json = os.path.join(PASTA_JSON, nome_json)
        with open(caminho_json, "w", encoding="utf-8") as j:
            json.dump(dados_finais, j, indent=4, ensure_ascii=False)

        # 2. Move o CSV original para não processar de novo
        shutil.move(caminho_in, os.path.join(PASTA_PROCESSADOS, nome_arquivo))
        
        print(f"✅ Sucesso! JSON gerado em: {caminho_json}")
        print(f"📦 CSV movido para a pasta de processados.\n")

    except Exception as e:
        print(f"💥 Erro ao processar {nome_arquivo}: {e}")

print("🛰️  Monitor de Fim de Corrida Ativado!")
print(f"Aguardando {TIMEOUT_FINALIZACAO}s de silêncio nos arquivos...")

while True:
    arquivos = [f for f in os.listdir(PASTA_ENTRADA) if f.endswith(".csv")]
    tempo_atual = time.time()

    for arq in arquivos:
        caminho_arquivo = os.path.join(PASTA_ENTRADA, arq)
        ultima_modificacao = os.path.getmtime(caminho_arquivo)
        segundos_desde_o_ultimo_dado = tempo_atual - ultima_modificacao

        # Se o arquivo parou de ser atualizado (fim da corrida)
        if segundos_desde_o_ultimo_dado > TIMEOUT_FINALIZACAO:
            print(f"🏁 Fim de corrida detectado para: {arq}")
            processar_arquivo_csv(arq)

    time.sleep(2) # Verifica a pasta a cada 2 segundos