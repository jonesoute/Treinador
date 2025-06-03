# utils/strava_api.py

import requests
import json
import os
from datetime import datetime, timedelta

CLIENT_ID = 162780
CLIENT_SECRET = "ced7a10bee89be4b576a815571f64c01f65dd85f"
REDIRECT_URI = "http://localhost:8501"
TOKEN_PATH = os.path.join("data", "strava_token.json")

AUTH_URL = f"https://www.strava.com/oauth/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&approval_prompt=force&scope=activity:read_all"

def token_existe():
    return os.path.exists(TOKEN_PATH)

def carregar_token():
    if token_existe():
        with open(TOKEN_PATH, "r") as f:
            return json.load(f)
    return None

def salvar_token(token):
    with open(TOKEN_PATH, "w") as f:
        json.dump(token, f)

def autenticar_usuario(code):
    url = "https://www.strava.com/oauth/token"
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code"
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        token_data = response.json()
        salvar_token(token_data)
        return token_data
    else:
        raise Exception("Erro ao autenticar com o Strava.")

def atualizar_token_expirado(token):
    if datetime.utcfromtimestamp(token["expires_at"]) < datetime.utcnow():
        print("Atualizando token expirado...")
        url = "https://www.strava.com/oauth/token"
        payload = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "refresh_token",
            "refresh_token": token["refresh_token"]
        }
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            new_token = response.json()
            salvar_token(new_token)
            return new_token
        else:
            raise Exception("Erro ao atualizar token.")
    return token

def buscar_atividades(dias=90):
    token = carregar_token()
    if not token:
        raise Exception("Token não encontrado.")
    token = atualizar_token_expirado(token)

    headers = {"Authorization": f"Bearer {token['access_token']}"}
    after = int((datetime.now() - timedelta(days=dias)).timestamp())
    url = f"https://www.strava.com/api/v3/athlete/activities?after={after}&per_page=200"

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Erro ao buscar atividades.")

