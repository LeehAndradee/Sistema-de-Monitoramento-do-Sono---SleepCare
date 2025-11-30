# core/views.py
from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Avg 
from django.utils import timezone 
from django.db.models.functions import ExtractWeekDay 
from datetime import timedelta 

from .models import RegistroSono
from .forms import RegistroSonoForm 


# -------------------------------------------------------------
# FUNÇÃO DE ANÁLISE (Utility)
# -------------------------------------------------------------
def get_weekly_sleep_metrics(user):
    """Calcula a média, o melhor e o pior dia de sono na última semana."""
    
    hoje = timezone.now().date()
    sete_dias_atras = hoje - timedelta(days=7)
    
    dados_semanais = RegistroSono.objects.filter(
        usuario=user,
        data_dormiu__date__gte=sete_dias_atras
    ).annotate(
        dia_da_semana=ExtractWeekDay('data_dormiu')
    )
    
    if not dados_semanais.exists():
        return None

    media_total = dados_semanais.aggregate(Avg('total_horas'))['total_horas__avg']

    media_por_dia = dados_semanais.values('dia_da_semana').annotate(
        avg_horas=Avg('total_horas')
    )
    
    MAPA_DIAS = {1: 'Domingo', 2: 'Segunda', 3: 'Terça', 4: 'Quarta', 5: 'Quinta', 6: 'Sexta', 7: 'Sábado'}

    melhor_dia_data = media_por_dia.order_by('-avg_horas').first()
    pior_dia_data = media_por_dia.order_by('avg_horas').first()

    metrics = {
        'media_semanal': f"{media_total:.1f}", 
        'melhor_dia': f"{MAPA_DIAS.get(melhor_dia_data['dia_da_semana'])} ({melhor_dia_data['avg_horas']:.1f}h)",
        'pior_dia': f"{MAPA_DIAS.get(pior_dia_data['dia_da_semana'])} ({pior_dia_data['avg_horas']:.1f}h)",
    }
    
    return metrics


# -------------------------------------------------------------
# FUNÇÕES DE AUTENTICAÇÃO
# -------------------------------------------------------------
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        # Usa o AuthenticationForm importado no topo
        form = AuthenticationForm(request, data=request.POST) 

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            context = {
                'titulo': 'Entrar no SleepCase',
                'form': form,
                'error_message': 'Credenciais inválidas. Tente novamente.'
            }
            return render(request, 'core/login.html', context)
    else:
        form = AuthenticationForm()
        
    context = {
        'titulo': 'Entrar no SleepCase',
        'form': form
    }
    return render(request, 'core/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('login') 


# -------------------------------------------------------------
# FUNÇÕES PRINCIPAIS DO APP
# -------------------------------------------------------------
@login_required 
def dashboard(request):
    registros = RegistroSono.objects.filter(usuario=request.user).order_by('-data_dormiu')[:7]
    metricas_semanais = get_weekly_sleep_metrics(request.user)

    context = {
        'titulo': 'Meu Dashboard - SleepCare',
        'registros_recentes': registros,
        'metricas': metricas_semanais,
    }
    return render(request, 'core/dashboard.html', context)


@login_required 
def registrar_sono(request):
    if request.method == 'POST':
        form = RegistroSonoForm(request.POST)
        if form.is_valid():
            registro = form.save(commit=False)
            registro.usuario = request.user 
            registro.save()
            return redirect('dashboard') 
    else:
        form = RegistroSonoForm()
    
    context = {
        'titulo': 'Registrar Novo Sono',
        'form': form
    }
    return render(request, 'core/registro_sono.html', context)


@login_required 
def dicas_higiene_sono(request):
    """Carrega o template com as dicas de higiene do sono."""
    # Dicas hardcoded. Mantenha esta função LIMPA (sem duplicação!)
    dicas = [
        {
            'titulo': 'Mantenha um Horário Consistente',
            'descricao': 'Vá para a cama e acorde no mesmo horário todos os dias, incluindo fins de semana. Isso regula o seu relógio biológico.',
            'icone': '⏰'
        },
        {
            'titulo': 'Otimize o Ambiente de Sono',
            'descricao': 'Certifique-se de que o seu quarto esteja escuro, silencioso e com uma temperatura agradável. Use cortinas blackout, se necessário.',
            'icone': '🛌'
        },
        {
            'titulo': 'Evite Cafeína e Nicotina',
            'descricao': 'Evite o consumo de cafeína (café, chás, refrigerantes) e nicotina pelo menos 4 a 6 horas antes de dormir.',
            'icone': '☕'
        },
        {
            'titulo': 'Limite Sonecas Diurnas',
            'descricao': 'Se precisar de sonecas, que sejam curtas (20-30 minutos) e não muito tarde, para não atrapalhar o sono noturno.',
            'icone': '😴'
        },
        {
            'titulo': 'Crie uma Rotina Relaxante',
            'descricao': 'Desenvolva um ritual de relaxamento antes de dormir: um banho quente, leitura de um livro físico ou meditação.',
            'icone': '🧘'
        },
        {
            'titulo': 'Evite Telas Luminosas',
            'descricao': 'Pare de usar smartphones, tablets ou computadores pelo menos uma hora antes de deitar. A luz azul inibe a melatonina.',
            'icone': '📱'
        },
    ]

    context = {
        'titulo': 'Tutorial - Dicas de Higiene do Sono',
        'dicas': dicas,
    }
    return render(request, 'core/dicas_higiene.html', context)

@login_required
def configuracoes_view(request):
    """
    Exibe a tela de configurações do perfil do usuário.
    """
    # Simula o texto para o Avatar (primeira letra do nome de usuário)
    avatar_text = request.user.username[0].upper() 
    
    context = {
        'titulo': 'Configurações de Conta',
        'avatar_text': avatar_text,
        # Em um projeto real, aqui você passaria formulários para edição
    }
    return render(request, 'core/configuracoes.html', context)