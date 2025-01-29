from django.urls import path,include
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('meu_perfil/', views.meu_perfil, name='meu_perfil'),
]