# utils/db_supabase.py

from supabase import create_client
import streamlit as st
from utils.logger import registrar_erro

# 🔑 Chaves do Supabase
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

# 🌐 Cliente Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 🔍 Verifica se o perfil existe por e-mail
def perfil_existe_supabase(email):
    try:
        result = supabase.table("usuarios").select("email").eq("email", email).execute()
        return len(result.data) > 0
    except Exception as e:
        registrar_erro(f"[Supabase] Erro ao verificar existência de '{email}': {e}")
        return False

# 📥 Carrega perfil completo por e-mail
def carregar_perfil_supabase(email):
    try:
        result = supabase.table("usuarios").select("*").eq("email", email).single().execute()
        return result.data
    except Exception as e:
        registrar_erro(f"[Supabase] Erro ao carregar perfil '{email}': {e}")
        return None

# 💾 Salva ou atualiza o perfil no Supabase
def salvar_perfil_supabase(email, dados):
    try:
        if perfil_existe_supabase(email):
            supabase.table("usuarios").update(dados).eq("email", email).execute()
        else:
            supabase.table("usuarios").insert(dados).execute()
        return True
    except Exception as e:
        registrar_erro(f"[Supabase] Erro ao salvar perfil '{email}': {e}")
        return False
