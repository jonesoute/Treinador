# utils/perfil.py

import os
import json
from datetime import date
from utils.logger import registrar_erro

def caminho_perfil(usuario_id):
    return os.path.join("data", "usuarios", usuario_id, "perfil.json")

def perfil_existe(usuario_id):
    return os.path.exists(caminho_perfil(usuario_id))

def carregar_perfil(usuario_id):
    try:
        caminho = caminho_perfil(usuario_id)
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        registrar_erro(f"Erro ao carregar perfil do usuário '{usuario_id}': {e}")
        return {
            "nome": usuario_id,
            "peso": 70,
            "altura": 170,
            "sexo": "Masculino",
            "dias_disponiveis": [],
            "horas_disponiveis": {},
            "modalidades": ["Ciclismo"],
            "ftp": 200,
            "preferencia_intensidade": "frequencia",
            "data_criacao": date.today().isoformat()
        }

def salvar_perfil(usuario_id, perfil):
    try:
        caminho = caminho_perfil(usuario_id)
        os.makedirs(os.path.dirname(caminho), exist_ok=True)
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(perfil, f, ensure_ascii=False, indent=4)
    except Exception as e:
        registrar_erro(f"Erro ao salvar perfil do usuário '{usuario_id}': {e}")
