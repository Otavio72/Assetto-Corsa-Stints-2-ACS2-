from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required
# Create your views here.

@csrf_exempt
def teste(request):
    #return JsonResponse({'status': 'EAEEEEE MANO DATA ? TUDO BAO ?'})
    
    if request.method == "POST":

        dados = json.loads(request.body)

        print("Recebi:")
        print(dados)

        return JsonResponse({
            "status": "ok"
        })

    return JsonResponse({
        "erro": "use POST"
    })


#@login_required
# Renderiza a página inicial do site
def index(request):
    return render(request, 'index.html')


# Renderiza a Pagina Quem Somos
def quemsomos(request):
    return render(request, 'quemsomos.html')


