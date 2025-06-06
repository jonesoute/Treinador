# utils/perfil.py

import json
from utils.db import conectar
from utils.logger import registrar_erro

def salvar_perfil(usuario_id, perfil):
    try:
        conn = conectar()
        cursor = conn.cursor()
        dados_json = json.dumps(perfil)
        cursor.execute("REPLACE INTO usuarios (id, dados) VALUES (?, ?)", (usuario_id, dados_json))
        conn.commit()
        conn.close()
    except Exception as e:
        registrar_erro(f"Erro ao salvar perfil '{usuario_id}': {e}")

def carregar_perfil(usuario_id):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT dados FROM usuarios WHERE id = ?", (usuario_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return json.loads(row[0])
        return None
    except Exception as e:
        registrar_erro(f"Erro ao carregar perfil '{usuario_id}': {e}")
        return None

def perfil_existe(usuario_id):
    return carregar_perfil(usuario_id) is not None
