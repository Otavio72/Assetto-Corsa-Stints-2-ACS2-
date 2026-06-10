from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
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

