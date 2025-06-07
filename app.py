# app.py

import streamlit as st
from components.login import exibir_login
from components.perfil_form import exibir_formulario_perfil
from components.dashboard import exibir_dashboard
from components.calendar import exibir_calendario_provas
from components.treino_card import exibir_treinos_semana
from utils.perfil import perfil_existe, carregar_perfil

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Treinador Virtual", layout="wide")

# ===== GERENCIAMENTO DE SESSÃO =====
if "usuario_id" not in st.session_state:
    st.session_state["usuario_id"] = None
if "primeiro_acesso" not in st.session_state:
    st.session_state["primeiro_acesso"] = False

# ===== TELA DE LOGIN =====
if not st.session_state["usuario_id"] and not st.session_state["primeiro_acesso"]:
    exibir_login()
    st.stop()

# ===== TELA DE PRIMEIRO ACESSO =====
if st.session_state.get("primeiro_acesso"):
    st.title("📝 Cadastro de Novo Atleta")
    perfil = exibir_formulario_perfil()
    if perfil:
        st.success("✅ Perfil salvo com sucesso!")
        st.session_state["primeiro_acesso"] = False
        st.experimental_rerun()
    st.stop()

# ===== USUÁRIO LOGADO =====
usuario_id = st.session_state["usuario_id"]

if not perfil_existe(usuario_id):
    st.info("Seu perfil ainda não está completo. Vamos preenchê-lo.")
    perfil = exibir_formulario_perfil()
    if perfil:
        st.success("✅ Perfil salvo com sucesso!")
        st.experimental_rerun()
    st.stop()
else:
    perfil = carregar_perfil(usuario_id)

# MENU LATERAL
st.sidebar.title("👤 Usuário")
st.sidebar.markdown(f"**{perfil.get('nome', 'Atleta')}**")

paginas = ["🏠 Início", "📊 Dashboard", "📆 Calendário", "🧠 Treinos da Semana", "⚙️ Perfil"]
pagina = st.sidebar.radio("Menu", paginas)

# ===== TELAS =====
if pagina == "🏠 Início":
    st.header(f"Bem-vindo, {perfil.get('nome')} 👋")
    conectar_strava_api(usuario_id)

elif pagina == "📊 Dashboard":
    exibir_dashboard(usuario_id, perfil.get("ftp", 200))

elif pagina == "📆 Calendário":
    exibir_calendario_provas(usuario_id)

elif pagina == "🧠 Treinos da Semana":
    exibir_treinos_semana(usuario_id)

elif pagina == "⚙️ Perfil":
    st.header("⚙️ Informações do Perfil")
    st.json(perfil)
    st.warning("A edição de perfil será atualizada em breve.")
