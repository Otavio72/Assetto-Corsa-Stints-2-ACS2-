import requests
import json


import requests
import json

from django.conf import settings

API_KEY = settings.GEMINI_API_KEY

def generate_gemini_report(context):
    
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent"

    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": API_KEY
    }

    prompt = f"""
Você é um engenheiro de corrida de um simulador de automobilismo.

Responda em português do Brasil.

Seja breve, claro e amigável.

Compare dois stints de corrida com base nos dados fornecidos.

Regras:
- máximo 6 a 8 linhas
- diga qual foi mais rápido
- diga qual foi mais consistente
- destaque a melhor volta de cada um
- finalize com um comentário leve e positivo (tom humano, quase fofo mesmo)

Não use linguagem longa nem técnica demais.

DADOS:
{context}
"""

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload)

    data = response.json()

    if "error" in data:
        return f"API ERROR: {data['error']}"

    return data["candidates"][0]["content"]["parts"][0]["text"]