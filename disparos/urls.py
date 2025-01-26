from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.disparar_mensagens, name='home'),
]