# utils/db_supabase.py

import os
from supabase import create_client, Client
from dotenv import load_dotenv
from utils.logger import registrar_erro

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def get_supabase_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = get_supabase_client()

def perfil_existe(usuario_id: str) -> bool:
    try:
        result = supabase.table("usuarios").select("id").eq("id", usuario_id).execute()
        return len(result.data) > 0
    except Exception as e:
        registrar_erro(f"Erro ao verificar existência do perfil '{usuario_id}': {e}")
        return False

def salvar_perfil(usuario_id: str, perfil: dict) -> bool:
    try:
        perfil_completo = {"id": usuario_id, **perfil}
        resposta = supabase.table("usuarios").insert(perfil_completo).execute()
        return bool(resposta.data)
    except Exception as e:
        registrar_erro(f"Erro ao salvar perfil '{usuario_id}': {e}")
        return False

def carregar_perfil(usuario_id: str) -> dict:
    try:
        resultado = supabase.table("usuarios").select("*").eq("id", usuario_id).limit(1).execute()
        if resultado.data:
            return resultado.data[0]
        else:
            return {}
    except Exception as e:
        registrar_erro(f"Erro ao carregar perfil '{usuario_id}': {e}")
        return {}

def atualizar_perfil(usuario_id: str, novos_dados: dict) -> bool:
    try:
        resposta = supabase.table("usuarios").update(novos_dados).eq("id", usuario_id).execute()
        return bool(resposta.data)
    except Exception as e:
        registrar_erro(f"Erro ao atualizar perfil '{usuario_id}': {e}")
        return False
