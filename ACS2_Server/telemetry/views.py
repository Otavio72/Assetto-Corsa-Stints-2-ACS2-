from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required
from usuarios.models import UserToken
from .models import Stint, TelemetryLap
from .schema import build_acs2_schema


@csrf_exempt
def teste(request):
    if request.method == "POST":

        dados = json.loads(request.body)

        session_uuid = dados.get("session_uuid")
        token = dados.get("token")

        if not session_uuid:
            return JsonResponse({"erro": "session_uuid faltando"}, status=400)

        user = UserToken.objects.get(token=token).user

        # =====================================================
        # 🟢 1. GARANTE QUE O STINT SEMPRE EXISTE
        # =====================================================
        stint, created = Stint.objects.get_or_create(
            session_uuid=session_uuid,
            defaults={
                "user": user,
                "game": dados.get("Jogo"),
                "car": dados.get("Carro"),
                "track": None,
                "status": "active"
            }
        )

        if created:
            print("🟢 HEADER CRIADO")

        # =====================================================
        # 🟡 2. ATUALIZA TRACK QUANDO CHEGAR
        # =====================================================
        track = dados.get("Pista")

        if track and track not in ["", "desconhecida", "unknown", "Desconhecida"]:
            if not stint.track:
                stint.track = track
                stint.save(update_fields=["track"])

        # =====================================================
        # 📡 3. TELEMETRIA (SEMPRE EXECUTA)
        # =====================================================
        normalized = build_acs2_schema(dados)

        if normalized.get("lap_number") is not None:

            TelemetryLap.objects.create(
                stint=stint,
                lap_number=normalized.get("lap_number"),
                lap_time=normalized.get("lap_time"),
                best_lap=normalized.get("best_lap"),
                driver_name=normalized.get("driver_name"),
                driver_slot=normalized.get("driver_slot"),
            )

            print("📡 TELEMETRIA")

        return JsonResponse({"status": "ok", "stint_id": stint.id})

    return JsonResponse({"erro": "use POST"}, status=405)


#@login_required
# Renderiza a página inicial do site
def index(request):
    return render(request, 'index.html')


# Renderiza a Pagina Quem Somos
def quemsomos(request):
    return render(request, 'quemsomos.html')


