from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Avg, Max, Min 
from django.utils import timezone
from django.db.models.functions import ExtractWeekDay
from datetime import timedelta
from django.contrib import messages # Certifique-se de que está importado

from .models import RegistroSono
from .forms import RegistroSonoForm


# -------------------------------------------------------------
# MÉTRICAS SEMANAIS (CORRIGIDO PARA total_horas_dormidas)
# -------------------------------------------------------------
def get_weekly_sleep_metrics(user):
    hoje = timezone.now().date()
    sete_dias_atras = hoje - timedelta(days=7)

    dados_semanais = RegistroSono.objects.filter(
        usuario=user,
        data_dormiu__date__gte=sete_dias_atras
    )

    if not dados_semanais.exists():
        return None
    
    # 🔹 1. Média Semanal (CORREÇÃO: Usando 'total_horas_dormidas')
    agregacao_geral = dados_semanais.aggregate(
        media=Avg('total_horas_dormidas'),
    )
    
    # 🔹 2. Média por Dia da Semana 
    medias_por_dia = dados_semanais.annotate(
        dia=ExtractWeekDay('data_dormiu') # 1=Domingo ... 7=Sábado
    ).values('dia').annotate(
        media_dia=Avg('total_horas_dormidas')
    ).order_by('dia')

    # Mapeamento do dia da semana 
    MAPA_DIAS = {
        1: "Domingo", 2: "Segunda", 3: "Terça", 4: "Quarta", 
        5: "Quinta", 6: "Sexta", 7: "Sábado"
    }
    
    # Encontra o melhor e pior dia
    melhor_dia_obj = max(medias_por_dia, key=lambda x: x['media_dia'])
    pior_dia_obj = min(medias_por_dia, key=lambda x: x['media_dia'])
    
    media_semanal = agregacao_geral['media']

    return {
        "media_semanal": f"{media_semanal:.1f}",
        "melhor_dia": f"{MAPA_DIAS[melhor_dia_obj['dia']]} ({melhor_dia_obj['media_dia']:.1f}h)",
        "pior_dia": f"{MAPA_DIAS[pior_dia_obj['dia']]} ({pior_dia_obj['media_dia']:.1f}h)",
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


@login_required
def dashboard(request):
    registros = RegistroSono.objects.filter(
        usuario=request.user
    ).order_by('-data_dormiu')[:7]

    metricas = get_weekly_sleep_metrics(request.user)

    # --- Dados para o gráfico Ideal vs Real ---
    labels = []
    horas_reais = []
    horas_ideais = []

    for r in registros[::-1]:  # inverte ordem para ficar cronológico
        labels.append(r.data_dormiu.strftime("%d/%m"))
        horas_reais.append(r.total_horas_dormidas)
        horas_ideais.append(8)  # meta fixa

    return render(request, 'core/dashboard.html', {
        'titulo': 'Meu Dashboard - SleepCare',
        'registros_recentes': registros,
        'metricas': metricas,
        'labels': labels,
        'horas_reais': horas_reais,
        'horas_ideais': horas_ideais
    })



# -------------------------------------------------------------
# REGISTRAR SONO (COM CÁLCULO DE DURAÇÃO)
# -------------------------------------------------------------
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