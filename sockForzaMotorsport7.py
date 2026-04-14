import socket
import struct

#UDP_IP = "127.0.0.1"
UDP_PORT = 5300


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", UDP_PORT))


while True:
            # Recebe dados do jogo
            data, addr = sock.recvfrom(4096)
            # Se o pacote for muito pequeno, ignora
            if len(data) < 228:
                print("Pacote muito pequeno, aguardando próximo...")
                continue
            
            try:
                # Extrai dados binários do pacote (offsets específicos)
                #current_rpm = struct.unpack_from('<f', data, 16)[0]
                #gear = struct.unpack_from('<B', data, 307)[0]
                #steer = struct.unpack_from('<b', data, 308)[0]
                #acelerador = struct.unpack_from('<B', data, 303)[0]
                #freio = struct.unpack_from('<B', data, 304)[0]
                velocidade = struct.unpack_from('<f', data, 244)[0] * 3.6
                #boost = struct.unpack_from('<f', data, 272)[0]
                bestlap = struct.unpack_from('<f', data, 284)[0]
                #racePosition = struct.unpack_from('<B', data, 302)[0]
                lapNumber = struct.unpack_from('<h', data, 300)[0]
                #fuel = struct.unpack_from('<f', data, 276)[0]
                #isRaceOn = struct.unpack_from('<i', data, 0)[0]
                #carroID = struct.unpack_from('<i', data, 212)[0]

                print(f"velocidade {velocidade}, bestlap {bestlap}, lapNumber {lapNumber}")
            except struct.error as e:
                print(f"Erro ao decodificar pacote: {e}")