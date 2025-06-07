# app.py

import streamlit as st
from components.login import exibir_login
from components.perfil_form import exibir_formulario_perfil
from utils.perfil import perfil_existe, carregar_perfil, salvar_perfil
from utils.strava_api import (
    token_existe,
    gerar_link_autenticacao,
    autenticar_usuario,
    coletar_e_salvar_atividades,
    carregar_atividades
)

# CONFIGURAÇÃO GERAL
st.set_page_config(page_title="Treinador Virtual", layout="wide")
st.title("🚴🏃 Treinador Virtual de Ciclismo e Corrida")

# LOGIN
usuario_id = exibir_login()
if not usuario_id and not st.session_state.get("primeiro_acesso"):
    st.stop()

# Se for primeiro acesso, mostra o formulário de perfil
if st.session_state.get("primeiro_acesso"):
    novo_perfil = exibir_formulario_perfil()
    if novo_perfil:
        from utils.perfil import salvar_perfil
        salvar_perfil(novo_perfil["id"], novo_perfil)
        st.success("✅ Perfil salvo com sucesso!")
        del st.session_state["primeiro_acesso"]
        st.session_state["usuario_id"] = novo_perfil["id"]
        st.rerun()
    st.stop()

# VERIFICAR SE PERFIL EXISTE
if not perfil_existe(usuario_id):
    st.info("Primeiro acesso: preencha seu perfil.")
    perfil = exibir_formulario_perfil(usuario_id)
    if perfil:
        salvar_perfil(usuario_id, perfil)
        st.success("✅ Perfil salvo com sucesso!")
        st.experimental_rerun()
    st.stop()
else:
    perfil = carregar_perfil(usuario_id)

# MENU LATERAL
st.sidebar.title("📂 Menu")
paginas = [
    "🏠 Início",
    "📅 Atividades",
    "📊 Dashboard",
    "📆 Calendário",
    "🧠 Treinos da Semana",
    "⚙️ Perfil"
]
pagina = st.sidebar.radio("Acesse uma seção:", paginas)

# ===== TELA: INÍCIO =====
if pagina == "🏠 Início":
    st.header(f"Bem-vindo, {perfil.get('nome')} 👋")

    # AUTENTICAÇÃO STRAVA
    st.subheader("🔗 Conexão com Strava")
    if not token_existe(usuario_id):
        st.warning("Sua conta ainda não está conectada ao Strava.")
        link = gerar_link_autenticacao()
        st.markdown(f"[🔗 Autorizar acesso ao Strava]({link})")

        code = st.text_input("Após autorizar, cole o código aqui:")
        if code:
            try:
                autenticado = autenticar_usuario(usuario_id, code)
                if autenticado:
                    st.success("✅ Conectado ao Strava com sucesso!")
                    st.experimental_rerun()
            except Exception as e:
                st.error(f"Erro ao autenticar com o Strava: {e}")
    else:
        st.success("Strava conectado ✅")

    st.subheader("📡 Importar treinos do Strava")
    if st.button("🔄 Atualizar treinos"):
        atividades = coletar_e_salvar_atividades(usuario_id)
        st.success(f"{len(atividades)} atividades importadas com sucesso.")

    st.subheader("📅 Gerar semana de treinos")
    if st.button("🧠 Gerar treinos da semana"):
        from utils.treino_generator import gerar_semana_treinos
        treinos = gerar_semana_treinos(usuario_id)
        st.success("✅ Plano semanal gerado com sucesso!")

# ===== TELA: ATIVIDADES =====
elif pagina == "📅 Atividades":
    st.header("📋 Últimas Atividades Salvas")
    atividades = carregar_atividades(usuario_id)
    if not atividades:
        st.warning("Nenhuma atividade encontrada. Atualize os treinos na tela inicial.")
    else:
        for a in atividades[:5]:
            tipo = a.get("type", "Ride")
            st.markdown(
                f"- **{a['name']}** | {a['distance']/1000:.1f} km | "
                f"{a['moving_time']//60} min | Tipo: {tipo} | {a.get('start_date_local', '')[:10]}"
            )

# ===== TELA: DASHBOARD =====
elif pagina == "📊 Dashboard":
    from components.dashboard import exibir_dashboard
    exibir_dashboard(usuario_id, perfil.get("ftp", 200))

# ===== TELA: CALENDÁRIO DE PROVAS =====
elif pagina == "📆 Calendário":
    from components.calendar import exibir_calendario_provas
    exibir_calendario_provas(usuario_id)

# ===== TELA: TREINOS DA SEMANA =====
elif pagina == "🧠 Treinos da Semana":
    from components.treino_card import exibir_treinos_semana
    exibir_treinos_semana(usuario_id)

# ===== TELA: PERFIL DO USUÁRIO =====
elif pagina == "⚙️ Perfil":
    st.header("⚙️ Informações do Perfil")
    st.json(perfil)
    st.warning("A edição do perfil será implementada em breve.")
