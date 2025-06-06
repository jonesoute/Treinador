# app.py

import streamlit as st
from utils.perfil import carregar_perfil, salvar_perfil, perfil_existe
from utils.strava_api import (
    token_existe,
    gerar_link_autenticacao,
    autenticar_usuario,
    coletar_e_salvar_atividades,
    carregar_atividades
)
from components.perfil_form import exibir_formulario_perfil

# CONFIGURAÇÃO
st.set_page_config(page_title="Treinador Virtual", layout="wide")
st.title("🏁 Treinador Virtual de Ciclismo e Corrida")

# IDENTIFICAÇÃO DO USUÁRIO
st.sidebar.header("👤 Identificação do Atleta")
usuario_id = st.sidebar.text_input("Digite seu nome de usuário", max_chars=30)

if not usuario_id:
    st.warning("Digite seu nome de usuário para continuar.")
    st.stop()

st.success(f"Usuário ativo: {usuario_id}")

# PERFIL
if not perfil_existe(usuario_id):
    st.info("Vamos configurar seu perfil.")
    perfil = exibir_formulario_perfil(usuario_id)
    if perfil:
        salvar_perfil(usuario_id, perfil)
        st.success("✅ Perfil salvo com sucesso! Recarregue a página para continuar.")
        st.stop()
else:
    perfil = carregar_perfil(usuario_id)

# AUTENTICAÇÃO STRAVA
st.sidebar.subheader("🔗 Conexão com Strava")
if not token_existe(usuario_id):
    st.sidebar.markdown("Conecte sua conta Strava para importar seus treinos:")
    link = gerar_link_autenticacao()
    st.sidebar.markdown(f"[🔗 Autorizar acesso ao Strava]({link})")

    try:
        autenticado = autenticar_usuario(usuario_id)
        if autenticado:
            st.success("✅ Strava conectado com sucesso!")
            st.experimental_rerun()
    except Exception as e:
        st.error(f"Erro ao autenticar: {e}")
        st.stop()
else:
    st.sidebar.success("Strava conectado ✅")

# MENU LATERAL
st.sidebar.title("📂 Menu")
modalidades = perfil.get("modalidades", ["Ciclismo"])
paginas = ["🏠 Início"]
if "Ciclismo" in modalidades or "Corrida" in modalidades:
    paginas.extend(["📅 Atividades", "📆 Calendário", "📊 Dashboard", "🧠 Treinos da Semana"])
paginas.append("⚙️ Perfil")
pagina = st.sidebar.radio("Acesse uma seção:", paginas)

# ===== TELAS =====
if pagina == "🏠 Início":
    st.header(f"Bem-vindo, {perfil['nome']} 👋")
    st.markdown("Use o menu lateral para navegar entre as funcionalidades do treinador virtual.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📡 Importar treinos do Strava")
        if st.button("🔄 Atualizar treinos"):
            atividades = coletar_e_salvar_atividades(usuario_id)
            st.success(f"{len(atividades)} atividades atualizadas com sucesso.")

    with col2:
        st.subheader("📅 Gerar semana de treinos")
        if st.button("🧠 Gerar Treinos da Semana"):
            from utils.treino_generator import gerar_semana_treinos
            treinos = gerar_semana_treinos(usuario_id)
            st.success("✅ Plano semanal gerado com sucesso!")

elif pagina == "📅 Atividades":
    st.header("📋 Últimas Atividades Salvas")
    atividades = carregar_atividades(usuario_id)
    if not atividades:
        st.warning("Nenhuma atividade foi encontrada. Atualize pelo botão na tela inicial.")
    else:
        st.write(f"Exibindo as últimas {min(5, len(atividades))} de {len(atividades)} atividades:")
        for a in atividades[:5]:
            tipo = a.get("type", "Ride")
            st.markdown(
                f"- **{a['name']}** | {a['distance']/1000:.1f} km | "
                f"{a['moving_time']//60} min | Tipo: {tipo} | {a.get('start_date_local', '')[:10]}"
            )

elif pagina == "📆 Calendário":
    from components.calendar import exibir_calendario_provas
    exibir_calendario_provas(usuario_id)

elif pagina == "📊 Dashboard":
    from components.dashboard import exibir_dashboard
    exibir_dashboard(usuario_id, perfil.get("ftp", 200))

elif pagina == "🧠 Treinos da Semana":
    from components.treino_card import exibir_treinos_semana
    exibir_treinos_semana(usuario_id)

elif pagina == "⚙️ Perfil":
    st.header("⚙️ Informações do Perfil")
    st.json(perfil)
    st.warning("A edição de perfil será implementada em breve.")
