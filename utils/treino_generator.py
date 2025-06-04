# utils/treino_generator.py

import os
import json
from datetime import date, timedelta
from utils.analysis import preparar_dataframe_atividades, calcular_cargas
from components.calendar import carregar_provas
from utils.perfil import carregar_perfil

def salvar_treinos_semana(usuario_id, treinos):
    caminho = os.path.join("data", "usuarios", usuario_id, "treinos_semana.json")
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(treinos, f, ensure_ascii=False, indent=4)

def gerar_semana_treinos(usuario_id):
    perfil = carregar_perfil(usuario_id)
    modalidades = perfil.get("modalidades", ["Ciclismo"])
    dias_disponiveis = perfil.get("dias_disponiveis", [])
    horas_disponiveis = perfil.get("horas_disponiveis", {})
    ftp = perfil.get("ftp", 200)
    
    df = preparar_dataframe_atividades(usuario_id, ftp)
    cargas = calcular_cargas(df)
    provas = carregar_provas(usuario_id)

    hoje = date.today()
    plano = {}

    for i in range(7):  # gera os próximos 7 dias
        dia = hoje + timedelta(days=i)
        nome_dia = dia.strftime("%A")
        if nome_dia not in dias_disponiveis:
            continue

        tempo_max = horas_disponiveis.get(nome_dia, 1.0)
        tipo_treino = "leve" if cargas["TSB"] < -10 else "moderado" if cargas["TSB"] < 10 else "intenso"

        plano[dia.isoformat()] = []

        for modalidade in modalidades:
            if modalidade == "Ciclismo":
                treino = gerar_treino_ciclismo(tipo_treino, tempo_max)
            elif modalidade == "Corrida":
                treino = gerar_treino_corrida(tipo_treino, tempo_max)
            else:
                continue
            plano[dia.isoformat()].append(treino)

    salvar_treinos_semana(usuario_id, plano)
    return plano

def gerar_treino_ciclismo(intensidade, tempo_horas):
    tempo_min = round(tempo_horas * 60)
    if intensidade == "leve":
        return {
            "modalidade": "Ciclismo",
            "tipo": "Recuperação ativa",
            "descricao": f"Pedalada leve contínua, Z1-Z2, {tempo_min} min.",
            "zona": "Z1-Z2",
            "tempo": tempo_min
        }
    elif intensidade == "moderado":
        return {
            "modalidade": "Ciclismo",
            "tipo": "Endurance + blocos",
            "descricao": f"{tempo_min - 30} min endurance + 3x5min Z4 com 5min Z2 entre blocos.",
            "zona": "Z2-Z4",
            "tempo": tempo_min
        }
    elif intensidade == "intenso":
        return {
            "modalidade": "Ciclismo",
            "tipo": "Intervalado",
            "descricao": f"Aquecimento 15min + 5x4min Z5 (3min Z2 entre) + cooldown.",
            "zona": "Z2-Z5",
            "tempo": tempo_min
        }

def gerar_treino_corrida(intensidade, tempo_horas):
    tempo_min = round(tempo_horas * 60)
    if intensidade == "leve":
        return {
            "modalidade": "Corrida",
            "tipo": "Trote regenerativo",
            "descricao": f"Corrida leve contínua, R1-R2, {tempo_min} min.",
            "zona": "R1-R2",
            "tempo": tempo_min
        }
    elif intensidade == "moderado":
        return {
            "modalidade": "Corrida",
            "tipo": "Fartlek moderado",
            "descricao": f"{tempo_min - 20} min em ritmo confortável + 6x1min forte com 1min leve.",
            "zona": "R2-R4",
            "tempo": tempo_min
        }
    elif intensidade == "intenso":
        return {
            "modalidade": "Corrida",
            "tipo": "Intervalado",
            "descricao": f"Aquecimento 10min + 4x5min ritmo forte (Z4-Z5) com 3min leve.",
            "zona": "R3-R5",
            "tempo": tempo_min
        }

