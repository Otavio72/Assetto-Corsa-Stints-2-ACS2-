import flet as ft
import subprocess
import sys
import threading
import json
import os
import shutil
import requests
import uuid

caminho_projeto = "logs_capturados"
ultimo_log = ""
processo_socket = None
dados_recebidos = {}
SESSION_UUID = None
TOKEN = None
CONFIG_PATH = "config.json"



def salvar_token(token):
    with open(CONFIG_PATH, "w") as f:
        json.dump({"token": token}, f)

def EnviarDjango(dados_telemetria):

    #global dados_recebidos

    if not dados_telemetria:
        return
    
    if TOKEN:
        dados_telemetria["token"] = TOKEN

    try:

        r = requests.post(
            "http://127.0.0.1:8000/api/teste/",
            json=dados_telemetria,
            timeout=5
        )

        print(f"Django respondeu: {r.status_code}")

    except:
        print(f"erro")



def main(page: ft.Page):

# =========================================================================
# 🧹 UTILITARIOS
# =========================================================================

    def carregar_token():
        global TOKEN

        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r") as f:
                data = json.load(f)
                TOKEN = data.get("token")
                return True

        return False
    def limpar_logs(e):
        for item in os.listdir(caminho_projeto):

            item_completo = os.path.join(
                caminho_projeto,
                item
            )

            try:

                if os.path.isfile(item_completo):

                    os.unlink(item_completo)

                elif os.path.isdir(item_completo):

                    shutil.rmtree(item_completo)


            except Exception as erro:

                print(
                    f"ERRO: {erro}",
                    flush=True
                )

        #print(
         #   "🧹 Logs apagados!",
          #  flush=True
        #)

        # =====================================================
        # ✅ STATUS VISUAL
        # =====================================================

        led_pacote.bgcolor = ft.Colors.BLUE_GREY_700

        txt_status_socket.value = "Pasta logs: LIMPA"

        txt_status_socket.color = ft.Colors.BLUE_GREY_200

        page.update()

        #print(
         #   "🧹 Logs apagados!",
          #  flush=True
        #)

    def ler_output_socket(processo_socket):
        global dados_recebidos, ultimo_log
        
        while True:

            linha = processo_socket.stdout.readline()

            if not linha:
                break
            
            linha = linha.strip()

            # 🔥 MUDAR STATUS AO RECEBER DADOS
            #txt_status_socket.value = "Socket: RECEBENDO DADOS"
            #txt_status_socket.color = ft.Colors.GREEN_400

            #led_pacote.bgcolor = ft.Colors.GREEN_400

            #page.update()

            print("DADO RECEBIDO:", linha)

            if linha.startswith("{"):
                dados_recebidos = json.loads(linha)
                #print("JSON OK:", dados_recebidos)
                tipo = dados_recebidos.get("TYPE")
                code = dados_recebidos.get("CODE")
                msg = dados_recebidos.get("MSG")
                #Dadosidget = dados_recebidos["DATA"]

                if tipo == "STATUS":

                    msg = dados_recebidos.get("MSG")

                    if msg != ultimo_log:

                        terminal_logs.controls.append(
                            ft.Text(
                                f"[STATUS] {msg}"
                            )
                        )

                        ultimo_log = msg

                    if code == "01":
                        led_pacote.bgcolor = ft.Colors.ORANGE_400
                        txt_status_socket.value = "Socket: INICIADO"
                        txt_status_socket.color = ft.Colors.ORANGE_400
                        
                    elif code == "02":
                        led_pacote.bgcolor = ft.Colors.GREEN_400
                        txt_status_socket.value = "Socket: RECEBENDO DADOS"
                        txt_status_socket.color = ft.Colors.GREEN_400

                    elif code == "03":
                        led_pacote.bgcolor = ft.Colors.BLUE_400
                        txt_status_socket.value = "Socket: CONECTADO"
                        txt_status_socket.color = ft.Colors.BLUE_400

                    elif code == "00":
                        led_pacote.bgcolor = ft.Colors.GREY_900
                        txt_status_socket.value = f"Socket: {msg}"
                        txt_status_socket.color = ft.Colors.RED_400

                    elif code == "05":
                        print("PISTA OK")

                    elif code == "06":
                        print("CARRO OK")

                    
                elif tipo == "TELEMETRIA":

                    if code == "07":
                        dados_telemetria = dados_recebidos["DATA"]
                        dados_telemetria["session_uuid"] = SESSION_UUID
                        
                        if "Carro" in dados_telemetria:
                            txt_carro.value = dados_telemetria["Carro"]

                        if "Pista" in dados_telemetria:
                            txt_pista.value = dados_telemetria["Pista"]

                        if "Tempo" in dados_telemetria:
                            txt_ultima_volta.value = f"{dados_telemetria['Tempo']:.3f}"

                        EnviarDjango(dados_telemetria)
                        print(dados_telemetria)
                    
                    elif code == "08":
                        dados_telemetria = dados_recebidos["DATA"]
                        dados_telemetria["session_uuid"] = SESSION_UUID

                        if "Carro" in dados_telemetria:
                            txt_carro.value = dados_telemetria["Carro"]

                        if "Pista" in dados_telemetria:
                            txt_pista.value = dados_telemetria["Pista"]

                        if "Tempo" in dados_telemetria:
                            txt_ultima_volta.value = dados_telemetria["Tempo"]
                            
                        EnviarDjango(dados_telemetria)
                        #print(dados_telemetria)
                    
                    elif code == "09":
                        dados_telemetria = dados_recebidos["DATA"]
                        dados_telemetria["session_uuid"] = SESSION_UUID

                        if "Carro" in dados_telemetria:
                            txt_carro.value = dados_telemetria["Carro"]

                        if "Pista" in dados_telemetria:
                            txt_pista.value = dados_telemetria["Pista"]

                        if "Tempo" in dados_telemetria:
                            txt_ultima_volta.value = dados_telemetria["Tempo"]
                            
                        EnviarDjango(dados_telemetria)
                        #print(dados_telemetria)

                    #page.update()
            
            page.update()

    def IniciarAC():
        global processo_socket, SESSION_UUID

        SESSION_UUID = str(uuid.uuid4())

        processo_socket = subprocess.Popen(
        [sys.executable, "sockAssettoCorsa.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8"
    )
        threading.Thread(
            target=ler_output_socket,
            args=(processo_socket,),
            daemon=True
        ).start()

        #print("PID criado:", processo_socket.pid)

    def IniciarF12013():
        
        global processo_socket, SESSION_UUID

        SESSION_UUID = str(uuid.uuid4())

        processo_socket = subprocess.Popen(
        [sys.executable, "SockF12013.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8"
    )
        threading.Thread(
            target=ler_output_socket,
            args=(processo_socket,),
            daemon=True
        ).start()

    def IniciarMM():

        global processo_socket, SESSION_UUID

        SESSION_UUID = str(uuid.uuid4())

        processo_socket = subprocess.Popen(
        [sys.executable, "sockMotorsportManager.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8"
    )
        threading.Thread(
            target=ler_output_socket,
            args=(processo_socket,),
            daemon=True
        ).start()

    # 🎨 Configurações
    page.title = "Assetto Corsa Stints 2 - ACS 2"
    page.theme_mode = ft.ThemeMode.DARK

    page.window.width = 850
    page.window.height = 600
    page.window.resizable = False

    page.padding = 20

    jogo_atual = ""

    txt_carro = ft.Text(
            "Aguardando...",
            size=16,
            weight=ft.FontWeight.BOLD
        )

    txt_ultima_volta = ft.Text(
            "--:--.---"
        )

    txt_pista = ft.Text(
            "Aguardando..."
        )

    terminal_logs = ft.ListView(
            expand=True,
            spacing=2,
            auto_scroll=True
        )

    painel_carro = ft.Container(
    content=ft.Column(
        [
            ft.Text("🏎️ CARRO"),
            txt_carro,
            ft.Divider(),
            ft.Text("⏱️ Última volta"),
            txt_ultima_volta
        ]
    ),
    width=180,
    height=220,
    padding=10,
    border=ft.border.all(1, ft.Colors.WHITE24),
    border_radius=10
)
    painel_terminal = ft.Container(
    content=terminal_logs,
    width=400,
    height=220,
    padding=10,
    bgcolor=ft.Colors.BLACK87,
    border=ft.border.all(1, ft.Colors.WHITE24),
    border_radius=10
)
    
    painel_pista = ft.Container(
    content=ft.Column(
        [
            ft.Text("🌍 PISTA"),
            txt_pista
        ]
    ),
    width=180,
    height=220,
    padding=10,
    border=ft.border.all(1, ft.Colors.WHITE24),
    border_radius=10
)

    # =========================================================================
    # 🚥 COMPONENTES
    # =========================================================================

    led_pacote = ft.Container(
        width=20,
        height=20,
        border_radius=10,
        bgcolor=ft.Colors.RED_400,
        animate=ft.Animation(
            200,
            ft.AnimationCurve.EASE_OUT
        )
    )

    txt_status_socket = ft.Text(
        "Socket: DESLIGADO",
        size=16,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.RED_400
    )

    txt_jogo_titulo = ft.Text(
        "",
        size=28,
        weight=ft.FontWeight.BOLD
    )

    # =========================================================================
    # 🔥 SOCKET
    # =========================================================================

    def alternar_socket(e):
        global processo_socket
        nonlocal jogo_atual


        if btn_ligar_sock.text == "LIGAR COLETOR":

            if jogo_atual == "F1 2013":
                IniciarF12013()
            elif jogo_atual == "Assetto Corsa":
                IniciarAC()
            elif jogo_atual == "Motorsport Manager":
                IniciarMM()

            btn_ligar_sock.text = "DESLIGAR COLETOR"
            btn_ligar_sock.bgcolor = ft.Colors.RED_700

            txt_status_socket.value = "Socket: INICIADO"
            txt_status_socket.color = ft.Colors.YELLOW

            led_pacote.bgcolor = ft.Colors.YELLOW
        
        else:

            if processo_socket:
                processo_socket.kill()
                processo_socket.wait(timeout=2)
                processo_socket = None
                #print("PID encerrando:", processo_socket.pid)

            #processo_socket.kill()

            

            #print("poll:", processo_socket.poll())

                btn_ligar_sock.text = "LIGAR COLETOR"
                btn_ligar_sock.bgcolor = ft.Colors.GREEN_700

                txt_status_socket.value = "Socket: DESLIGADO"
                txt_status_socket.color = ft.Colors.RED_400

                led_pacote.bgcolor = ft.Colors.RED_400

        page.update()
        

    # =========================================================================
    # 🔘 BOTÃO
    # =========================================================================

    btn_ligar_sock = ft.ElevatedButton(
        text="LIGAR COLETOR",
        bgcolor=ft.Colors.GREEN_700,
        color=ft.Colors.WHITE,
        height=50,
        on_click=alternar_socket
    )

    # =========================================================================
    # 🗺️ ROTAS
    # =========================================================================

    def rota_mudou(route):

        page.views.clear()

        def fazer_login(e):

            global TOKEN
            try:
                r = requests.post(
                    "http://127.0.0.1:8000/usuarios/login_local/",
                    json={
                        "username": txt_user.value,
                        "password": txt_pass.value
                    }
                )

                data = r.json()

                if data.get("status") == "ok":

                    TOKEN = data["token"]
                    salvar_token(TOKEN)

                    page.go("/")

                else:
                    txt_erro.value = "Login inválido"
                    page.update()

            except Exception as ex:
                txt_erro.value = "Erro ao conectar com servidor"
                page.update()

        # ==========================================================
        # 🏁 MENU
        # ==========================================================

        if page.route == "/login":

            txt_user = ft.TextField(label="Usuário")
            txt_pass = ft.TextField(label="Senha", password=True)
            txt_erro = ft.Text(color="red")

            btn_login = ft.ElevatedButton(
                "Entrar",
                on_click=fazer_login
            )

            page.views.append(
                ft.View(
                    "/login",
                    [
                        ft.Text("ACS2 Login", size=30, weight=ft.FontWeight.BOLD),

                        txt_user,
                        txt_pass,

                        btn_login,

                        txt_erro
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
        elif page.route == "/":

            btn_sel_f1 = ft.TextButton(
                text="Selecionar",
                on_click=lambda _: ir_para_dashboard("F1 2013")
            )

            btn_sel_ac = ft.TextButton(
                text="Selecionar",
                on_click=lambda _: ir_para_dashboard("Assetto Corsa")
            )

            btn_sel_MM = ft.TextButton(
                text="Selecionar",
                on_click=lambda _: ir_para_dashboard("Motorsport Manager")
            )

            page.views.append(
                ft.View(
                    "/",
                    [
                        ft.AppBar(
                            title=ft.Text("ACS 2 - Selecione o Jogo"),
                            bgcolor=ft.Colors.SURFACE
                        ),

                        ft.Text(
                            "Escolha a categoria para iniciar a telemetria:",
                            size=18
                        ),

                        ft.Container(height=20),

                        ft.Row(
                            [
                                # CARD F1
                                ft.Card(
                                    content=ft.Container(
                                        content=ft.Column(
                                            [
                                                ft.ListTile(
                                                    leading=ft.Icon(ft.Icons.SPEED),
                                                    title=ft.Text("F1 2013"),
                                                    subtitle=ft.Text("Codemasters UDP Socket")
                                                ),

                                                ft.Row(
                                                    [btn_sel_f1],
                                                    alignment=ft.MainAxisAlignment.END
                                                )
                                            ]
                                        ),

                                        width=230,
                                        padding=10
                                    )
                                ),

                                # CARD AC
                                ft.Card(
                                    content=ft.Container(
                                        content=ft.Column(
                                            [
                                                ft.ListTile(
                                                    leading=ft.Icon(ft.Icons.DIRECTIONS_CAR),
                                                    title=ft.Text("Assetto Corsa"),
                                                    subtitle=ft.Text("Shared Memory / UDP")
                                                ),

                                                ft.Row(
                                                    [btn_sel_ac],
                                                    alignment=ft.MainAxisAlignment.END
                                                )
                                            ]
                                        ),

                                        width=230,
                                        padding=10
                                    )
                                ),

                                # CARD AC
                                ft.Card(
                                    content=ft.Container(
                                        content=ft.Column(
                                            [
                                                ft.ListTile(
                                                    leading=ft.Icon(ft.Icons.DIRECTIONS_CAR),
                                                    title=ft.Text("Motorsport Manager"),
                                                    subtitle=ft.Text("Arquivos")
                                                ),

                                                ft.Row(
                                                    [btn_sel_MM],
                                                    alignment=ft.MainAxisAlignment.END
                                                )
                                            ]
                                        ),

                                        width=230,
                                        padding=10
                                    )
                                )
                            ],

                            
                            spacing=20
                        )
                    ],

                                    )
            )

        # ==========================================================
        # 📊 DASHBOARD
        # ==========================================================

        elif page.route == "/dashboard":

            txt_jogo_titulo.value = f"Painel de Controle - {jogo_atual}"

            btn_voltar = ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                on_click=lambda _: page.go("/")
            )

            botoes_dashboard = [btn_ligar_sock]

            if jogo_atual == "Motorsport Manager":

                btn_limpar_logs = ft.ElevatedButton(
                    text="🧹 Limpar Logs",
                    bgcolor=ft.Colors.ORANGE_700,
                    color=ft.Colors.WHITE,
                    on_click=limpar_logs
    )

                botoes_dashboard.append(btn_limpar_logs)

            page.views.append(
                ft.View(
                    "/dashboard",
                    [
                        ft.AppBar(
                            title=txt_jogo_titulo,
                            bgcolor=ft.Colors.SURFACE,
                            leading=btn_voltar
                        ),

                        ft.Container(height=20),

                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.Text(
                                                "Status do Sinal:",
                                                size=16
                                            ),

                                            led_pacote,

                                            txt_status_socket
                                        ],

                                        
                                        spacing=15
                                    ),

                                    ft.Container(height=30),

                                    ft.Row(
                                        botoes_dashboard,
                                        spacing=20
                                                                            )
                                ]
                            ),

                            padding=30,

                            border=ft.border.all(
                                1,
                                ft.Colors.WHITE24
                            ),

                            border_radius=10,

                            bgcolor=ft.Colors.BLACK26
                        ),

                        ft.Container(height=5),

                        ft.Container(height=5),

                            ft.Row(
                                [
                                    painel_carro,
                                    painel_terminal,
                                    painel_pista
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=20
                            ),

                            ft.Container(height=10),

                        ft.Text(
                            "Dica: Ligue o coletor e depois abra o simulador na pista.",
                            size=12,
                            color=ft.Colors.WHITE38,
                            text_align=ft.TextAlign.CENTER
                        )
                    ],

                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )

        page.update()

    # =========================================================================
    # 🚗 NAVEGAÇÃO
    # =========================================================================

    def ir_para_dashboard(nome_jogo):

        nonlocal jogo_atual

        jogo_atual = nome_jogo

        page.go("/dashboard")

    def view_pop(view):

        page.views.pop()

        top_view = page.views[-1]

        page.go(top_view.route)

    page.on_route_change = rota_mudou
    page.on_view_pop = view_pop

    #page.go("/")

    if carregar_token():
        page.go("/")
    else:
        page.go("/login")


# 🚀 EXECUTA
ft.app(target=main)