from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required
from usuarios.models import UserToken
from .models import Stint, TelemetryLap
from .schema import build_acs2_schema
from .assets import get_track_image, get_car_image
from .utils.gemini import generate_gemini_report



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

@login_required
def AssettoCorsa(request):

    game = "Assetto Corsa"

    #stints = Stint.objects.filter(game=game).order_by("-id")
    
    stints = Stint.objects.filter(
        game=game,
        user=request.user
    ).order_by("-id")

    for stint in stints:
        stint.track_image = get_track_image(stint.track)
        stint.car_image = get_car_image(stint.car)

    return render(request, "assettocorsa.html", {
        "stints": stints,
        "game": game
    })


@login_required
def f12013(request):

    game = "F1 2013"
    
    stints = Stint.objects.filter(
        game=game,
        user=request.user
    ).order_by("-id")

    for stint in stints:
        stint.track_image = get_track_image(stint.track)
        stint.car_image = get_car_image(stint.car)

    return render(request, "F12013.html", {
        "stints": stints,
        "game": game
    })


@login_required
def motorsportmanager(request):
    game = "Motorsport Manager"
    
    stints = Stint.objects.filter(
        game=game,
        user=request.user
    ).order_by("-id")

    for stint in stints:
        stint.track_image = get_track_image(stint.track)
        stint.car_image = get_car_image(stint.car)

    return render(request, "MotorsportManager.html", {
        "stints": stints,
        "game": game
    })

@login_required
def analise(request, game, stint_a, stint_b):

    stint_a = Stint.objects.get(id=stint_a, game=game)
    stint_b = Stint.objects.get(id=stint_b, game=game)

    laps_a = TelemetryLap.objects.filter(stint=stint_a).order_by("lap_number")
    laps_b = TelemetryLap.objects.filter(stint=stint_b).order_by("lap_number")

    laps_a_data = [
        {"lap": l.lap_number, "time": l.lap_time}
        for l in laps_a
    ]

    laps_b_data = [
        {"lap": l.lap_number, "time": l.lap_time}
        for l in laps_b
    ]

    context = {
        "game": game,
        "track": stint_a.track,
        "car_a": stint_a.car,
        "car_b": stint_b.car,
        "laps_a": laps_a_data,
        "laps_b": laps_b_data,
    }

    report = generate_gemini_report(context)
    

    return render(request, "analise.html", {
        "game": game,
        "stint_a": stint_a,
        "stint_b": stint_b,
        "laps_a": json.dumps(laps_a_data),
        "laps_b": json.dumps(laps_b_data),
        "report": report,
        "car_a": stint_a.car,
        "car_b": stint_b.car,
    })

def about(request):
    return render(request, 'about.html')


