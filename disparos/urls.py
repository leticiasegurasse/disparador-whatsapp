from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('meus_chats/', views.meus_chats, name='meus_chats'),
    path('disparos/', views.disparar_mensagens, name='disparos'),
    path('historico/', views.listar_disparos, name='historico_disparos'),
    path('financeiro/', views.financeiro, name='financeiro'),
    path('ajuda/', views.ajuda, name='ajuda'),
]