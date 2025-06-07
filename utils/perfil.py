# utils/perfil.py

from utils.perfil import salvar_perfil, carregar_perfil
from utils.logger import registrar_erro

# 🔒 Verifica se perfil existe na Supabase
def perfil_existe(usuario_id):
    try:
        return perfil_existe_supabase(usuario_id)
    except Exception as e:
        registrar_erro(f"Erro ao verificar existência do perfil '{usuario_id}': {e}")
        return False

# 📥 Carrega perfil completo da Supabase
def carregar_perfil(usuario_id):
    try:
        return carregar_perfil_supabase(usuario_id)
    except Exception as e:
        registrar_erro(f"Erro ao carregar perfil '{usuario_id}': {e}")
        return None

# 💾 Salva/Atualiza perfil do usuário na Supabase
def salvar_perfil(usuario_id, dados):
    try:
        return salvar_perfil_supabase(usuario_id, dados)
    except Exception as e:
        registrar_erro(f"Erro ao salvar perfil '{usuario_id}': {e}")
        return False

# 🔐 Verifica login com e-mail e senha
def verificar_login(email, senha):
    try:
        perfil = carregar_perfil(email)
        if not perfil:
            return False
        return perfil.get("senha") == senha
    except Exception as e:
        registrar_erro(f"Erro ao verificar login de '{email}': {e}")
        return False
