# utils/strava_api.py

import os
import json
import requests
import streamlit as st
from datetime import datetime, timedelta
from utils.logger import registrar_erro

CLIENT_ID = st.secrets["STRAVA_CLIENT_ID"]
CLIENT_SECRET = st.secrets["STRAVA_CLIENT_SECRET"]
REDIRECT_URI = "https://nome-do-app.streamlit.app"  # Substitua pelo endereço real do seu app

def caminho_token(usuario_id):
    return os.path.join("data", "usuarios", usuario_id, "token.json")

def token_existe(usuario_id):
    return os.path.exists(caminho_token(usuario_id))

def salvar_token(usuario_id, token_info):
    try:
        caminho = caminho_token(usuario_id)
        os.makedirs(os.path.dirname(caminho), exist_ok=True)
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(token_info, f, ensure_ascii=False, indent=4)
    except Exception as e:
        registrar_erro(f"Erro ao salvar token Strava: {e}")

def carregar_token(usuario_id):
    try:
        with open(caminho_token(usuario_id), "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        registrar_erro(f"Erro ao carregar token Strava: {e}")
        return None

def gerar_link_autenticacao():
    return (
        f"https://www.strava.com/oauth/authorize"
        f"?client_id={CLIENT_ID}"
        f"&response_type=code"
        f"&redirect_uri={REDIRECT_URI}"
        f"&approval_prompt=auto"
        f"&scope=read,activity:read_all"
    )

def autenticar_usuario(usuario_id):
    query_params = st.query_params
    if "code" not in query_params:
        return False

    code = query_params["code"]

    try:
        response = requests.post("https://www.strava.com/oauth/token", data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code"
        })

        if response.status_code == 200:
            token_info = response.json()
            salvar_token(usuario_id, token_info)
            return True
        else:
            registrar_erro(f"Erro ao autenticar: {response.text}")
            return False

    except Exception as e:
        registrar_erro(f"Exceção na autenticação: {e}")
        return False

def coletar_e_salvar_atividades(usuario_id, dias=90):
    try:
        token = carregar_token(usuario_id)
        if not token:
            return []

        # Refresh token se necessário
        if datetime.utcfromtimestamp(token["expires_at"]) < datetime.utcnow():
            response = requests.post("https://www.strava.com/oauth/token", data={
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "grant_type": "refresh_token",
                "refresh_token": token["refresh_token"]
            })

            if response.status_code == 200:
                token = response.json()
                salvar_token(usuario_id, token)
            else:
                registrar_erro("Erro ao renovar token Strava.")
                return []

        headers = {"Authorization": f"Bearer {token['access_token']}"}
        after_timestamp = int((datetime.utcnow() - timedelta(days=dias)).timestamp())
        response = requests.get(
            f"https://www.strava.com/api/v3/athlete/activities?after={after_timestamp}&per_page=100",
            headers=headers
        )

        if response.status_code == 200:
            atividades = response.json()
            caminho = os.path.join("data", "usuarios", usuario_id, "atividades.json")
            os.makedirs(os.path.dirname(caminho), exist_ok=True)
            with open(caminho, "w", encoding="utf-8") as f:
                json.dump(atividades, f, ensure_ascii=False, indent=4)
            return atividades
        else:
            registrar_erro(f"Erro ao coletar atividades: {response.text}")
            return []

    except Exception as e:
        registrar_erro(f"Erro ao coletar atividades: {e}")
        return []

def carregar_atividades(usuario_id):
    caminho = os.path.join("data", "usuarios", usuario_id, "atividades.json")
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    return []
