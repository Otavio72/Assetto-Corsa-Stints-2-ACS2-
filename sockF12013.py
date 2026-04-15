import socket
import struct

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 20777))

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
    vel_kmh    = pacote[7] * 3.6
    tempo_lap  = pacote[1]
    gas        = pacote[29] * 100  # Convertendo para 0-100%
    brake      = pacote[31] * 100  # Convertendo para 0-100%
    pos        = int(pacote[39])
    total_laps = int(pacote[60])

    # --- Organização Visual ---
    # Criando barras visuais para os pedais (opcional, mas fica irado!)
    bar_gas = "█" * int(gas / 10)
    bar_brk = "█" * int(brake / 10)

    # O print formatado
    # \r no início faz ele voltar para o começo da linha
    print(f" 🏁 POS: {pos:02d} | VOLTA: {tempo_lap:6.2f}s | VEL: {vel_kmh:5.1f} km/h | TOTAL: {total_laps:02d} ", end="")
    print(f" | GAS: [{bar_gas:<10}] | FRE: [{bar_brk:<10}]", end="\r")