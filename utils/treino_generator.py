# utils/treino_generator.py

import os
import json
from datetime import date, timedelta, datetime
from utils.analysis import preparar_dataframe_atividades, calcular_cargas
from components.calendar import carregar_provas
from utils.perfil import carregar_perfil

def salvar_treinos_semana(usuario_id, treinos):
    caminho = os.path.join("data", "usuarios", usuario_id, "treinos_semana.json")
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(treinos, f, ensure_ascii=False, indent=4)

def carregar_feedbacks(usuario_id):
    caminho = os.path.join("data", "usuarios", usuario_id, "feedbacks.json")
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def ajustar_carga_por_feedback(usuario_id):
    feedbacks = carregar_feedbacks(usuario_id)
    hoje = date.today()
    ultima_semana = [hoje - timedelta(days=i) for i in range(1, 8)]

    valores_rpe = {
        "Muito fácil": 1,
        "Fácil": 2,
        "Moderado": 3,
        "Difícil": 4,
        "Exaustivo": 5
    }

    rpes = []
    for fb in feedbacks.values():
        data_fb = datetime.fromisoformat(fb["data"]).date()
        if data_fb in ultima_semana:
            rpes.append(valores_rpe.get(fb["sentimento"], 3))

    if not rpes:
        return 0, True

    media = sum(rpes) / len(rpes)
    if media <= 2.0:
        return +1, False
    elif media >= 4.0:
        return -1, False
    else:
        return 0, False

def obter_fase_treinamento(usuario_id):
    perfil = carregar_perfil(usuario_id)
    data_inicio = perfil.get("data_criacao", date.today().isoformat())
    data_inicio = datetime.fromisoformat(data_inicio).date()
    hoje = date.today()
    semanas = (hoje - data_inicio).days // 7

    provas = carregar_provas(usuario_id)
    provas_ordenadas = sorted(provas, key=lambda p: p["data_inicio"])
    if provas_ordenadas:
        data_prova = datetime.fromisoformat(provas_ordenadas[0]["data_inicio"]).date()
        semanas_ate_prova = (data_prova - hoje).days // 7

        if semanas_ate_prova <= 1:
            return "taper"
        elif semanas_ate_prova <= 3:
            return "pre-prova"

    if semanas < 4:
        return "base"
    elif semanas < 8:
        return "especifica"
    elif semanas < 10:
        return "pre-prova"
    else:
        return "transicao"

def gerar_semana_treinos(usuario_id):
    perfil = carregar_perfil(usuario_id)
    modalidades = perfil.get("modalidades", ["Ciclismo"])
    dias_disponiveis = perfil.get("dias_disponiveis", [])
    horas_disponiveis = perfil.get("horas_disponiveis", {})
    ftp = perfil.get("ftp", 200)

    df = preparar_dataframe_atividades(usuario_id, ftp)
    cargas = calcular_cargas(df)
    fase = obter_fase_treinamento(usuario_id)
    ajuste_feedback, sem_feedback = ajustar_carga_por_feedback(usuario_id)

    hoje = date.today()
    plano = {}

    if sem_feedback:
        plano["_mensagem"] = (
            "⚠️ Você não registrou nenhum feedback nos últimos 7 dias. "
            "A intensidade dos treinos será mantida sem ajustes automáticos. "
            "Responder aos feedbacks permite que o plano se adapte melhor ao seu corpo e evolução."
        )

    for i in range(7):
        dia = hoje + timedelta(days=i)
        nome_dia = dia.strftime("%A")
        if nome_dia not in dias_disponiveis:
            continue

        tempo_max = horas_disponiveis.get(nome_dia, 1.0)
        tipo_treino = "leve" if cargas["TSB"] < -10 else "moderado" if cargas["TSB"] < 10 else "intenso"

        if fase == "base" and tipo_treino == "intenso":
            tipo_treino = "moderado"
        elif fase in ["taper", "transicao"]:
            tipo_treino = "leve"

        if ajuste_feedback == +1 and tipo_treino == "moderado":
            tipo_treino = "intenso"
        elif ajuste_feedback == -1 and tipo_treino == "intenso":
            tipo_treino = "moderado"
        elif ajuste_feedback == -1 and tipo_treino == "moderado":
            tipo_treino = "leve"

        plano[dia.isoformat()] = []
        for modalidade in modalidades:
            if modalidade == "Ciclismo":
                treino = gerar_treino_ciclismo(tipo_treino, tempo_max, fase)
            elif modalidade == "Corrida":
                treino = gerar_treino_corrida(tipo_treino, tempo_max, fase)
            plano[dia.isoformat()].append(treino)

    salvar_treinos_semana(usuario_id, plano)
    return plano

def gerar_treino_ciclismo(intensidade, tempo_horas, fase="base"):
    tempo_min = round(tempo_horas * 60)
    if intensidade == "leve":
        return {
            "modalidade": "Ciclismo",
            "tipo": f"Recuperação ativa ({fase})",
            "descricao": f"Pedalada leve contínua, Z1-Z2, {tempo_min} min.",
            "zona": "Z1-Z2",
            "tempo": tempo_min,
            "fase": fase
        }
    elif intensidade == "moderado":
        return {
            "modalidade": "Ciclismo",
            "tipo": f"Endurance com blocos ({fase})",
            "descricao": f"{tempo_min - 30}min Z2 + 3x5min Z4 com 5min Z2.",
            "zona": "Z2-Z4",
            "tempo": tempo_min,
            "fase": fase
        }
    elif intensidade == "intenso":
        return {
            "modalidade": "Ciclismo",
            "tipo": f"Intervalado intenso ({fase})",
            "descricao": f"15min Z2 + 5x4min Z5 (3min Z2 entre) + cooldown.",
            "zona": "Z2-Z5",
            "tempo": tempo_min,
            "fase": fase
        }

def gerar_treino_corrida(intensidade, tempo_horas, fase="base"):
    tempo_min = round(tempo_horas * 60)
    if intensidade == "leve":
        return {
            "modalidade": "Corrida",
            "tipo": f"Trote regenerativo ({fase})",
            "descricao": f"Corrida leve contínua, R1-R2, {tempo_min} min.",
            "zona": "R1-R2",
            "tempo": tempo_min,
            "fase": fase
        }
    elif intensidade == "moderado":
        return {
            "modalidade": "Corrida",
            "tipo": f"Fartlek moderado ({fase})",
            "descricao": f"{tempo_min - 20}min ritmo confortável + 6x1min forte.",
            "zona": "R2-R4",
            "tempo": tempo_min,
            "fase": fase
        }
    elif intensidade == "intenso":
        return {
            "modalidade": "Corrida",
            "tipo": f"Intervalado forte ({fase})",
            "descricao": f"10min aquecimento + 4x5min ritmo forte + cooldown.",
            "zona": "R3-R5",
            "tempo": tempo_min,
            "fase": fase
        }
