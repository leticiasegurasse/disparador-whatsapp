import csv
import json
import requests
import random
import time
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import DisparoHistorico
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model

User = get_user_model()  # Obtém o modelo correto de usuário


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required
def meus_chats(request):
    return render(request, 'chats.html')


@login_required
def disparar_mensagens(request):
    # Recupera a API key do usuário logado
    api_key = request.user.api_key

    if request.method == 'POST':
        mensagem = request.POST.get('mensagem')
        csv_file = request.FILES.get('csv_file')
        intervalo_opcao = request.POST.get('intervalo_opcao')

        if not csv_file:
            return render(request, 'disparar.html', {
                'status': 'error',
                'message': 'Arquivo CSV não encontrado.',
                'api_key': api_key
            })

        try:
            # Define os intervalos baseados na opção selecionada
            intervalo_opcoes = {
                '0-5': (0, 300),
                '5-15': (300, 900),
                '15-25': (900, 1500)
            }
            intervalo_min, intervalo_max = intervalo_opcoes.get(intervalo_opcao, (None, None))

            if intervalo_min is None:
                return render(request, 'disparar.html', {
                    'status': 'error',
                    'message': 'Opção de intervalo inválida.',
                    'api_key': api_key
                })

            # Lê o arquivo CSV com delimitador ";"
            csv_data = list(csv.reader(csv_file.read().decode('utf-8').splitlines(), delimiter=';'))

            # Verifica se há pelo menos uma linha válida no arquivo
            if len(csv_data) == 0:
                return render(request, 'disparar.html', {
                    'status': 'error',
                    'message': 'O arquivo CSV está vazio.',
                    'api_key': api_key
                })

            url = f"https://disparador-evolution-api.t615yd.easypanel.host/message/sendText/{request.user.instancia}"
            headers = {"Content-Type": "application/json", "apikey": api_key}

            total_linhas = len(csv_data)

            for index, row in enumerate(csv_data):
                # Verifica se a linha contém pelo menos dois campos
                if len(row) < 2:
                    print(f"Linha {index + 1} ignorada por estar incompleta: {row}")
                    continue  # Pula essa linha se estiver mal formatada

                # Gera o intervalo aleatório dentro do intervalo escolhido apenas se houver mais de 2 linhas
                if total_linhas >= 2 and index > 0:
                    intervalo_espera = random.randint(intervalo_min, intervalo_max)
                    print(f"Aguardando {intervalo_espera} segundos antes do próximo envio...")
                    time.sleep(intervalo_espera)

                phoneNumber, name = row[:2]

                mensagem_formatada = f"{mensagem}".replace("{name}", name)
                postData = {
                    "number": f"55{phoneNumber}",
                    "text": mensagem_formatada
                }

                try:
                    response = requests.post(url, json=postData, headers=headers)
                    response.raise_for_status()
                    status = 'success'
                    print(f"Mensagem enviada com sucesso para {name} ({phoneNumber})")
                except requests.RequestException:
                    status = 'error'
                    print(f"Erro ao enviar para {name} ({phoneNumber}): {str(e)}")

                # Salva no banco de dados
                DisparoHistorico.objects.create(
                    usuario=request.user,
                    numero=phoneNumber,
                    nome=name,
                    mensagem=mensagem,
                    status=status
                )
                

            # Renderiza a página com uma mensagem de sucesso
            return render(request, 'disparar.html', {
                'status': 'success',
                'message': 'Mensagens enviadas com sucesso!',
                'api_key': api_key
            })

        except Exception as e:
            # Renderiza a página com a mensagem de erro
            return render(request, 'disparar.html', {
                'status': 'error',
                'message': f'Erro ao enviar mensagens: {str(e)}',
                'api_key': api_key
            })

    return render(request, 'disparar.html', {'api_key': api_key})


@login_required
def listar_disparos(request):
    # Obtém todos os usuários para o filtro (apenas para administradores)
    usuarios = User.objects.all() if request.user.is_staff else None

    # Verifica se o usuário é do setor administrativo
    if request.user.is_staff:
        usuario_id = request.GET.get('usuario')  # ID do usuário selecionado no filtro
        if usuario_id:
            disparos = DisparoHistorico.objects.filter(usuario_id=usuario_id).order_by('-data_envio')
        else:
            disparos = DisparoHistorico.objects.all().order_by('-data_envio')
    else:
        # Usuários não administrativos só podem ver seus próprios disparos
        disparos = DisparoHistorico.objects.filter(usuario=request.user).order_by('-data_envio')

    # Paginação
    paginator = Paginator(disparos, 10)  # 10 disparos por página
    page_number = request.GET.get('page')  # Número da página na URL
    page_obj = paginator.get_page(page_number)

    return render(request, 'listar_disparos.html', {
        'page_obj': page_obj,
        'is_admin': request.user.is_staff,
        'usuarios': usuarios,  # Envia a lista de usuários para o template
    })



@login_required
def financeiro(request):
    return render(request, 'financeiro.html')


@login_required
def ajuda(request):
    return render(request, 'ajuda.html')
