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

    teste1 = pacote[45]
    teste2 = pacote[46]
    teste3 = pacote[47]
    teste4 = pacote[48]
    teste5 = pacote[49]
    teste6 = pacote[50]

    #print()
    print(f"teste: {teste1} // teste: {teste2}  // teste: {teste3} // teste: {teste4} // teste: {teste5} // teste: {teste6}")