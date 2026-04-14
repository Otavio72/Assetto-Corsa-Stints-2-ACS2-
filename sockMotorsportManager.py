import os
import shutil
import time

# --- CONFIGURAÇÃO ---
caminho_jogo = r"C:\Games\Motorsport Manager"
caminho_projeto = r"./logs_capturados" # Pasta onde você vai guardar os arquivos

# Cria a pasta de destino se ela não existir
if not os.path.exists(caminho_projeto):
    os.makedirs(caminho_projeto)

print("🏎️  Bot de Captura ACS 2: Ativado!")
print("Aguardando arquivos .csv aparecerem...")

while True:
    # Lista todos os arquivos .csv na pasta do jogo
    arquivos = [f for f in os.listdir(caminho_jogo) if f.endswith(".csv")]

    for arquivo in arquivos:
        origem = os.path.join(caminho_jogo, arquivo)
        
        # Criamos um nome com timestamp para não sobrescrever o anterior no seu projeto
        novo_nome = f"{int(time.time())}_{arquivo}"
        destino = os.path.join(caminho_projeto, novo_nome)

        try:
            # O 'move' já tira da pasta do jogo e joga na sua
            shutil.move(origem, destino)
            print(f"✅ Capturado: {arquivo} -> {novo_nome}")
        except PermissionError:
            # Se o jogo estiver escrevendo, ele ignora e tenta no próximo segundo
            pass
        except Exception as e:
            print(f"❌ Erro ao mover: {e}")

    # Checa a pasta a cada 1 segundo
    time.sleep(1)