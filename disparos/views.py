import csv
import json
import requests
import time
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required
def disparar_mensagens(request):
    if request.method == 'POST':
        mensagem = request.POST.get('mensagem')
        csv_file = request.FILES.get('csv_file')
        intervalo_de_espera = int(request.POST.get('intervalo', 5))

        if not csv_file:
            return JsonResponse({'status': 'error', 'message': 'Arquivo CSV não encontrado.'})

        try:
            # Lê o arquivo CSV
            csv_data = csv.reader(csv_file.read().decode('utf-8').splitlines())
            url = 'https://disparador-evolution-api.t615yd.easypanel.host//message/sendText/leticia'
            api_key = '602Goa6v7h7J9ZSO6sceffJLzWKDcoCT'
            headers = {"Content-Type": "application/json", "apikey": api_key}

            for row in csv_data:
                phoneNumber, name = row[0], row[1]
                postData = {
                    "number": f"55{phoneNumber}",
                    "text": f"Olá, {name}!\n\n{mensagem}"
                }
                response = requests.post(url, json=postData, headers=headers)
                response.raise_for_status()
                time.sleep(intervalo_de_espera)

            return JsonResponse({'status': 'success', 'message': 'Mensagens enviadas com sucesso!'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return render(request, 'disparar.html')
