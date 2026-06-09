import os

# --- COLOQUE O CAMINHO DO ARQUIVO QUE QUER ANALISAR AQUI ---
arquivo_para_analisar = r"C:\Users\otavi\OneDrive\Área de Trabalho\COMPUTADOR\PROJETOS\Assetto Corsa Stints 2\logs_capturados\1776880086_TrackSessionData.csv"

def mapear_colunas(caminho):
    try:
        if not os.path.exists(caminho):
            print(f"❌ Erro: Arquivo não encontrado em: {caminho}")
            return

        with open(caminho, mode='r', encoding='utf-8') as f:
            # Pegamos apenas a primeira linha (o cabeçalho)
            linha_cabecalho = f.readline().strip()
            
            # Limpamos aspas e dividimos pela vírgula
            colunas = [c.replace('"', '').strip() for c in linha_cabecalho.split(",")]
            
            print(f"\n📊 ESTRUTURA DO ARQUIVO: {os.path.basename(caminho)}")
            print("-" * 50)
            for i, nome in enumerate(colunas):
                print(f"Índice {i}  ==>  {nome}")
            print("-" * 50)
            print(f"Total de colunas detectadas: {len(colunas)}\n")

    except Exception as e:
        print(f"❌ Ocorreu um erro ao ler o arquivo: {e}")

# Executa a função
mapear_colunas(arquivo_para_analisar)