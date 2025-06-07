# utils/perfil.py

from utils.db_supabase import supabase
from utils.logger import registrar_erro

def perfil_existe(usuario_id):
    try:
        result = supabase.table("usuarios").select("id").eq("id", usuario_id).execute()
        return len(result.data) > 0
    except Exception as e:
        registrar_erro(f"[perfil_existe] Erro: {e}")
        return False

def carregar_perfil(usuario_id):
    try:
        result = supabase.table("usuarios").select("*").eq("id", usuario_id).execute()
        if result.data:
            return result.data[0]
        return {}
    except Exception as e:
        registrar_erro(f"[carregar_perfil] Erro: {e}")
        return {}

def salvar_perfil(usuario_id, perfil):
    try:
        perfil["id"] = usuario_id
        if perfil_existe(usuario_id):
            supabase.table("usuarios").update(perfil).eq("id", usuario_id).execute()
        else:
            supabase.table("usuarios").insert(perfil).execute()
    except Exception as e:
        registrar_erro(f"[salvar_perfil] Erro ao salvar perfil '{usuario_id}': {e}")
