# utils/analysis.py

import os
import json
import pandas as pd
from datetime import datetime
from utils.logger import registrar_erro

def carregar_atividades(usuario_id):
    try:
        caminho = os.path.join("data", "usuarios", usuario_id, "atividades.json")
        if os.path.exists(caminho):
            with open(caminho, "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    except Exception as e:
        registrar_erro(f"Erro ao carregar atividades do usuário '{usuario_id}' para análise: {e}")
        return []

def preparar_dataframe_atividades(usuario_id, ftp):
    try:
        atividades = carregar_atividades(usuario_id)
        dados = []
        for a in atividades:
            if a.get("type") not in ["Ride", "Run"]:
                continue

            distancia_km = a["distance"] / 1000 if "distance" in a else 0
            tempo_min = a["moving_time"] / 60 if "moving_time" in a else 0
            potencia = a.get("average_watts", None)
            hr = a.get("average_heartrate", None)
            data = a.get("start_date_local", "")[:10]

            if not data or tempo_min == 0:
                continue

            tss = 0
            if potencia and ftp:
                int_rel = potencia / ftp
                tss = int((tempo_min * int_rel**2) / 60 * 100)
            elif hr:
                zonas = [(100, 1.0), (90, 0.9), (80, 0.8), (70, 0.7)]
                for limite, fator in zonas:
                    if hr >= limite:
                        tss = int(tempo_min * fator)
                        break

            dados.append({
                "data": data,
                "tipo": a["type"],
                "nome": a.get("name", ""),
                "distancia_km": round(distancia_km, 1),
                "tempo_min": round(tempo_min),
                "tss": tss
            })

        return pd.DataFrame(dados)

    except Exception as e:
        registrar_erro(f"Erro ao preparar dataframe de atividades de '{usuario_id}': {e}")
        return pd.DataFrame()

def calcular_cargas(df):
    try:
        df["data"] = pd.to_datetime(df["data"])
        df = df.sort_values("data")
        df = df.set_index("data")

        df["TSS"] = df["tss"]
        df["ATL"] = df["TSS"].rolling(window=7).mean().fillna(0)
        df["CTL"] = df["TSS"].rolling(window=42).mean().fillna(0)
        df["TSB"] = df["CTL"] - df["ATL"]

        ultimos = df.tail(1).to_dict(orient="records")[0]
        return {
            "ATL": round(ultimos.get("ATL", 0)),
            "CTL": round(ultimos.get("CTL", 0)),
            "TSB": round(ultimos.get("TSB", 0))
        }
    except Exception as e:
        registrar_erro(f"Erro ao calcular cargas de treino: {e}")
        return {"ATL": 0, "CTL": 0, "TSB": 0}
