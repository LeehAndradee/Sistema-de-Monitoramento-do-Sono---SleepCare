# core/urls.py (Certifique-se de que a rota esteja na lista urlpatterns)

from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'), 
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    path('cadastro/', views.cadastro_view, name='cadastro'),


    path('registrar-sono/', views.registrar_sono, name='registrar_sono'),
    path('dicas/', views.dicas_higiene_sono, name='dicas_higiene'),
]





