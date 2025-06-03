# app.py

import streamlit as st
from utils.perfil import carregar_perfil, salvar_perfil, perfil_existe
from components.perfil_form import exibir_formulario_perfil

# Configuração da página
st.set_page_config(page_title="Treinador Virtual de Ciclismo", layout="wide")

# Verificar se o perfil já foi preenchido
if not perfil_existe():
    perfil = exibir_formulario_perfil()
    if perfil:
        salvar_perfil(perfil)
        st.success("✅ Perfil salvo com sucesso! Recarregue a página para continuar.")
        st.stop()
else:
    perfil = carregar_perfil()
    st.sidebar.title("🚴 Navegação")
    pagina = st.sidebar.radio("Selecione a seção", ["🏠 Início", "📅 Treinos", "📊 Dashboard", "⚙️ Perfil"])

    if pagina == "🏠 Início":
        st.title(f"Bem-vindo, {perfil['nome']} 👋")
        st.markdown("Use o menu lateral para acessar seus treinos, visualizar o dashboard ou ajustar seu perfil.")

    elif pagina == "📅 Treinos":
        st.header("📅 Aqui será exibido o calendário de treinos e competições.")
        st.info("Esta seção será implementada nas próximas fases.")

    elif pagina == "📊 Dashboard":
        st.header("📊 Seu painel de métricas e desempenho.")
        st.info("Esta seção será implementada nas próximas fases.")

    elif pagina == "⚙️ Perfil":
        st.header("⚙️ Editar Perfil")
        st.warning("A edição de perfil ainda será implementada.")

