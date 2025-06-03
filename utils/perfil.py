# utils/perfil.py

import json
import os

BASE_DIR = "data/usuarios"

def caminho_perfil(usuario_id):
    return os.path.join(BASE_DIR, usuario_id, "perfil.json")

def salvar_perfil(usuario_id: str, perfil: dict) -> None:
    """Salva o perfil do usuário."""
    dir_usuario = os.path.join(BASE_DIR, usuario_id)
    os.makedirs(dir_usuario, exist_ok=True)
    with open(caminho_perfil(usuario_id), "w", encoding="utf-8") as f:
        json.dump(perfil, f, ensure_ascii=False, indent=4)

def carregar_perfil(usuario_id: str) -> dict:
    """Carrega o perfil salvo para um usuário específico."""
    caminho = caminho_perfil(usuario_id)
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def perfil_existe(usuario_id: str) -> bool:
    """Verifica se já existe perfil salvo para o usuário."""
    return os.path.exists(caminho_perfil(usuario_id))
