def build_acs2_schema(dados):

    schema = {
        # identidade
        "session_uuid": dados.get("session_uuid"),
        "token": dados.get("token"),
        "game": dados.get("Jogo"),

        # corrida
        "track": dados.get("Pista"),
        "layout": dados.get("Layout"),

        # veículo
        "car": dados.get("Carro"),

        # pilotos (MM)
        "driver_1": dados.get("NomePiloto1"),
        "driver_2": dados.get("NomePiloto2"),

        # performance
        "lap_number": dados.get("Volta") or dados.get("VoltaAtual"),
        "lap_time": dados.get("Tempo"),
        "best_lap": dados.get("BestLap"),

        # F1 específico
        "remaining_laps": dados.get("Restantes"),

        # fallback
        "extra": dados
    }

    if dados.get("Jogo") == "Motorsport Manager":

        if dados.get("NomePiloto1"):
            schema["driver_name"] = dados.get("NomePiloto1")
            schema["driver_slot"] = 1

        elif dados.get("NomePiloto2"):
            schema["driver_name"] = dados.get("NomePiloto2")
            schema["driver_slot"] = 2

    return schema