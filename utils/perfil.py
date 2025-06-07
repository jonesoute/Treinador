# utils/perfil.py

from utils.db_supabase import (
    salvar_perfil_supabase,
    carregar_perfil_supabase,
    perfil_existe_supabase
)

def salvar_perfil(usuario_id: str, perfil: dict) -> bool:
    return salvar_perfil_supabase(usuario_id, perfil)

def carregar_perfil(usuario_id: str) -> dict:
    return carregar_perfil_supabase(usuario_id)

def perfil_existe(usuario_id: str) -> bool:
    return perfil_existe_supabase(usuario_id)
