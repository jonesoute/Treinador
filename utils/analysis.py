# utils/analysis.py

import os
import json
from datetime import datetime, timedelta
import math
import pandas as pd

def carregar_atividades(usuario_id):
    caminho = os.path.join("data", "usuarios", usuario_id, "atividades.json")
    if not os.path.exists(caminho):
        return []
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)

def calcular_tss(atividade, ftp=200, esporte="Ride"):
    """Calcula ou estima o TSS de uma atividade com base no tipo de esporte."""
    duracao_seg = atividade.get("moving_time", 0)
    duracao_horas = duracao_seg / 3600
    intensidade = 0.6  # valor base

    if esporte == "Ride":
        media_potencia = atividade.get("average_watts")
        if media_potencia and ftp:
            intensidade = media_potencia / ftp
        elif atividade.get("average_heartrate"):
            fc = atividade["average_heartrate"]
            intensidade = 0.5 + (fc - 120) / 100

    elif esporte == "Run":
        pace = atividade.get("average_speed", 0)  # em m/s
        if pace:
            ritmo_kmph = pace * 3.6
            intensidade = 0.65 + (ritmo_kmph - 9) / 20  # baseado em ritmo acima de ~5:30/km
        if atividade.get("average_heartrate"):
            fc = atividade["average_heartrate"]
            intensidade += (fc - 130) / 150

    intensidade = max(0.4, min(intensidade, 1.6))  # controle de limites

    tss = duracao_horas * (intensidade ** 2) * 100
    return round(tss, 1)

def preparar_dataframe_atividades(usuario_id, ftp=200, tipo=None):
    atividades = carregar_atividades(usuario_id)
    dados = []

    for a in atividades:
        tipo_atividade = a.get("type", "Ride")
        if tipo and tipo_atividade != tipo:
            continue

        if not a.get("start_date_local"):
            continue

        data = datetime.fromisoformat(a["start_date_local"].replace("Z", ""))
        tss = calcular_tss(a, ftp, tipo_atividade)
        dados.append({
            "data": data.date(),
            "nome": a.get("name"),
            "duracao_min": round(a.get("moving_time", 0) / 60),
            "tss": tss,
            "tipo": tipo_atividade
        })

    df = pd.DataFrame(dados)
    df = df.sort_values("data")
    return df

def calcular_cargas(df, data_final=None):
    """Calcula ATL, CTL e TSB com base nos TSS das atividades filtradas."""
    if df.empty:
        return {"ATL": 0, "CTL": 0, "TSB": 0}

    if data_final is None:
        data_final = df["data"].max()

    data_final = pd.to_datetime(data_final)
    df["data"] = pd.to_datetime(df["data"])

    atl = df[(df["data"] >= data_final - timedelta(days=6))]["tss"].mean()
    ctl = df[(df["data"] >= data_final - timedelta(days=41))]["tss"].mean()
    tsb = ctl - atl

    return {
        "ATL": round(atl if not math.isnan(atl) else 0, 1),
        "CTL": round(ctl if not math.isnan(ctl) else 0, 1),
        "TSB": round(tsb if not math.isnan(tsb) else 0, 1),
    }
