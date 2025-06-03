# utils/perfil.py

import json
import os

# Caminho padrão do arquivo de perfil
PERFIL_PATH = os.path.join("data", "perfil_usuario.json")

def salvar_perfil(perfil: dict) -> None:
    """Salva o perfil do usuário em JSON."""
    with open(PERFIL_PATH, "w", encoding="utf-8") as f:
        json.dump(perfil, f, ensure_ascii=False, indent=4)

def carregar_perfil() -> dict:
    """Carrega o perfil salvo, se existir. Caso contrário, retorna None."""
    if os.path.exists(PERFIL_PATH):
        with open(PERFIL_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def perfil_existe() -> bool:
    """Verifica se já existe perfil salvo."""
    return os.path.exists(PERFIL_PATH)

