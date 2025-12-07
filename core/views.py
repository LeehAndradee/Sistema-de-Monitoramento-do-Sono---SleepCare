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
# MÉTRICAS SEMANAIS
# -------------------------------------------------------------
def get_weekly_sleep_metrics(user):
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

    media_total = dados_semanais.aggregate(
        Avg('total_horas')
    )['total_horas__avg']

    media_por_dia = dados_semanais.values('dia_da_semana').annotate(
        avg_horas=Avg('total_horas')
    )

    MAPA_DIAS = {
        1: 'Domingo', 2: 'Segunda', 3: 'Terça', 4: 'Quarta',
        5: 'Quinta', 6: 'Sexta', 7: 'Sábado'
    }

    melhor = media_por_dia.order_by('-avg_horas').first()
    pior = media_por_dia.order_by('avg_horas').first()

    return {
        'media_semanal': f"{media_total:.1f}",
        'melhor_dia': f"{MAPA_DIAS[melhor['dia_da_semana']]} ({melhor['avg_horas']:.1f}h)",
        'pior_dia': f"{MAPA_DIAS[pior['dia_da_semana']]} ({pior['avg_horas']:.1f}h)",
    }


# -------------------------------------------------------------
# LOGIN
# -------------------------------------------------------------
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            login(request, form.get_user())
            return redirect('dashboard')

        return render(request, 'core/login.html', {
            'titulo': 'Entrar no SleepCare',
            'form': form,
            'error_message': 'Credenciais inválidas.'
        })

    return render(request, 'core/login.html', {
        'titulo': 'Entrar no SleepCare',
        'form': AuthenticationForm()
    })


def logout_view(request):
    logout(request)
    return redirect('login')


# -------------------------------------------------------------
# DASHBOARD
# -------------------------------------------------------------
@login_required
def dashboard(request):
    registros = RegistroSono.objects.filter(usuario=request.user)[:7]
    metricas = get_weekly_sleep_metrics(request.user)

    return render(request, 'core/dashboard.html', {
        'titulo': 'Meu Dashboard - SleepCare',
        'registros_recentes': registros,
        'metricas': metricas
    })


# -------------------------------------------------------------
# REGISTRAR SONO
# -------------------------------------------------------------
from django.contrib import messages

@login_required
def registrar_sono(request):
    if request.method == 'POST':
        form = RegistroSonoForm(request.POST)
        if form.is_valid():
            registro = form.save(commit=False)
            registro.usuario = request.user
            registro.save()
            messages.success(request, "Registro salvo com sucesso!")
            return redirect('registrar_sono')
        else:
            messages.error(request, "Erro ao salvar registro.")
    else:
        form = RegistroSonoForm()

    return render(request, 'core/registro_sono.html', {'form': form})


# -------------------------------------------------------------
# DICAS DE HIGIENE DO SONO
# -------------------------------------------------------------
@login_required
def dicas_higiene_sono(request):
    dicas = [
        {
            'titulo': 'Mantenha um horário consistente',
            'descricao': 'Durma e acorde no mesmo horário.',
            'icone': '⏰'
        },
        {
            'titulo': 'Evite telas antes de dormir',
            'descricao': 'A luz azul atrapalha o sono.',
            'icone': '📱'
        }
    ]

    return render(request, 'core/dicas_higiene.html', {
        'titulo': 'Higiene do Sono',
        'dicas': dicas
    })


# -------------------------------------------------------------
# CONFIGURAÇÕES
# -------------------------------------------------------------
@login_required
def configuracoes_view(request):
    avatar = request.user.username[0].upper()

    return render(request, 'core/configuracoes.html', {
        'titulo': 'Configurações',
        'avatar_text': avatar
    })
