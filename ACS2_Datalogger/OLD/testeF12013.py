import socket

import struct

import sys



# Cores e comandos de terminal

RESET = "\033[0m"

CYAN = "\033[96m"

GREEN = "\033[92m"

YELLOW = "\033[93m"

RED = "\033[91m"

BOLD = "\033[1m"

HOME = "\033[H" # Move o cursor para o topo (0,0) sem limpar a tela



sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind(("0.0.0.0", 20777))



# Limpa a tela uma única vez no início

print("\033[2J", end="")



try:

    while True:

        data, addr = sock.recvfrom(2048)

        pacote = struct.unpack('f' * (len(data) // 4), data)

       

        # Montamos toda a string na memória antes de printar

        output = f"{HOME}{BOLD}{CYAN}=== [ ACS 2: DASHBOARD DE TELEMETRIA ] ==={RESET}\n"

        output += f"{YELLOW}Monitorando: {len(pacote)} índices | F1 2013 Ativo{RESET}\n\n"

       

        colunas = 5

        indices_para_mostrar = 150 # Foco nos primeiros 150 índices

       

        for i in range(0, indices_para_mostrar, colunas):

            linha = ""

            for j in range(colunas):

                idx = i + j

                if idx < len(pacote):

                    val = pacote[idx]

                   

                    # Lógica de destaque

                    cor_val = RESET

                    if idx == 2: cor_val = YELLOW + BOLD # Nossa âncora

                    elif 1.0 <= val <= 25.0 and val % 1 == 0: cor_val = RED + BOLD # IDs?

                    elif val == 0: cor_val = GREEN # Zeros

                   

                    str_val = f"{val:8.2f}" if abs(val) < 10000 else f"{val:8.1e}"

                    linha += f"{CYAN}{idx:03d}{RESET}:{cor_val}{str_val}{RESET} | "

            output += linha + "\n"

           

        output += "\n" + "-" * 75 + "\n"

        output += f"{BOLD}FOCO:{RESET} Procure valores {RED}RED{RESET} que mudam só quando você troca de pista.\n"

        output += f"Ex: Se em Interlagos [XX] é 14.00 e em Monza vira 11.00, achamos!"



        # Printa tudo de uma vez só atualizando o que já existe

        sys.stdout.write(output)

        sys.stdout.flush()



except KeyboardInterrupt:

    print(f"\n\n{RED}🛑 Scanner parado.{RESET}")