# utils/strava_api.py

import os
import json
import requests
import streamlit as st
from datetime import datetime, timedelta
from utils.logger import registrar_erro

CLIENT_ID = st.secrets["STRAVA_CLIENT_ID"]
CLIENT_SECRET = st.secrets["STRAVA_CLIENT_SECRET"]
REDIRECT_URI = "https://treinadorvirtualapp.streamlit.app"

def caminho_token(usuario_id):
    return os.path.join("data", "usuarios", usuario_id, "token.json")

def caminho_atividades(usuario_id):
    return os.path.join("data", "usuarios", usuario_id, "atividades.json")

def token_existe(usuario_id):
    return os.path.exists(caminho_token(usuario_id))

def gerar_link_autenticacao():
    return (
        f"https://www.strava.com/oauth/authorize?client_id={CLIENT_ID}"
        f"&response_type=code&redirect_uri={REDIRECT_URI}"
        f"&approval_prompt=force&scope=read,activity:read"
    )

def autenticar_usuario(usuario_id, code):
    try:
        url = "https://www.strava.com/oauth/token"
        payload = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code"
        }
        response = requests.post(url, data=payload)
        response.raise_for_status()
        token_data = response.json()

        os.makedirs(os.path.dirname(caminho_token(usuario_id)), exist_ok=True)
        with open(caminho_token(usuario_id), "w", encoding="utf-8") as f:
            json.dump(token_data, f)

    except Exception as e:
        registrar_erro(f"Erro ao autenticar usuário '{usuario_id}' com Strava: {e}")
        raise

def atualizar_token(usuario_id):
    try:
        with open(caminho_token(usuario_id), "r", encoding="utf-8") as f:
            token_data = json.load(f)

        expires_at = token_data.get("expires_at", 0)
        if datetime.utcnow().timestamp() < expires_at:
            return token_data

        payload = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "refresh_token",
            "refresh_token": token_data["refresh_token"]
        }

        response = requests.post("https://www.strava.com/oauth/token", data=payload)
        response.raise_for_status()
        token_data = response.json()

        with open(caminho_token(usuario_id), "w", encoding="utf-8") as f:
            json.dump(token_data, f)

        return token_data

    except Exception as e:
        registrar_erro(f"Erro ao atualizar token do usuário '{usuario_id}': {e}")
        return None

def coletar_e_salvar_atividades(usuario_id):
    try:
        token_data = atualizar_token(usuario_id)
        if not token_data:
            raise Exception("Token inválido ou não encontrado.")

        headers = {"Authorization": f"Bearer {token_data['access_token']}"}
        url = "https://www.strava.com/api/v3/athlete/activities"
        params = {"per_page": 200, "page": 1, "after": (datetime.now() - timedelta(days=90)).timestamp()}

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        atividades = response.json()

        caminho = caminho_atividades(usuario_id)
        os.makedirs(os.path.dirname(caminho), exist_ok=True)
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(atividades, f, ensure_ascii=False, indent=4)

        return atividades

    except Exception as e:
        registrar_erro(f"Erro ao coletar atividades do Strava para '{usuario_id}': {e}")
        return []

def carregar_atividades(usuario_id):
    try:
        caminho = caminho_atividades(usuario_id)
        if os.path.exists(caminho):
            with open(caminho, "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    except Exception as e:
        registrar_erro(f"Erro ao carregar atividades de '{usuario_id}': {e}")
        return []
