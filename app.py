# app.py

import streamlit as st
from utils.perfil import carregar_perfil, salvar_perfil, perfil_existe
from utils.strava_api import (
    token_existe,
    carregar_token,
    gerar_link_autenticacao,
    autenticar_usuario,
    buscar_atividades
)
from components.perfil_form import exibir_formulario_perfil

# CONFIGURAÇÕES GERAIS
st.set_page_config(page_title="Treinador Virtual de Ciclismo", layout="wide")
st.title("🚴 Treinador Virtual de Ciclismo")

# LOGIN DO USUÁRIO
st.sidebar.header("👤 Identificação do Atleta")
usuario_id = st.sidebar.text_input("Digite seu nome de usuário", max_chars=30)

if not usuario_id:
    st.warning("Digite seu nome de usuário para continuar.")
    st.stop()

st.success(f"Usuário ativo: {usuario_id}")

# FLUXO DE PERFIL
if not perfil_existe(usuario_id):
    st.info("Vamos configurar seu perfil.")
    perfil = exibir_formulario_perfil()
    if perfil:
        salvar_perfil(usuario_id, perfil)
        st.success("✅ Perfil salvo com sucesso! Recarregue a página para continuar.")
        st.stop()
else:
    perfil = carregar_perfil(usuario_id)

# FLUXO DE AUTENTICAÇÃO STRAVA
st.sidebar.subheader("🔗 Conexão com Strava")

if not token_existe(usuario_id):
    st.sidebar.markdown("Conecte sua conta Strava para importar seus treinos:")
    link = gerar_link_autenticacao()
    st.sidebar.markdown(f"[🔗 Autorizar acesso ao Strava]({link})")

    code = st.sidebar.text_input("Após autorizar, cole o código aqui:")

    if code:
        try:
            autenticar_usuario(usuario_id, code)
            st.success("✅ Strava conectado com sucesso!")
            st.experimental_rerun()
        except Exception as e:
            st.error(f"Erro ao autenticar: {e}")
            st.stop()
else:
    st.sidebar.success("Strava conectado ✅")

    # CARREGAR ATIVIDADES (exibição simples por enquanto)
    st.header("📋 Últimos Treinos (últimos 90 dias)")
    try:
        atividades = buscar_atividades(usuario_id)
        st.write(f"Foram encontradas {len(atividades)} atividades.")
        for a in atividades[:5]:  # mostra só os 5 mais recentes
            st.markdown(f"- **{a['name']}** | {a['distance']/1000:.1f} km | {a['moving_time']//60} min")
    except Exception as e:
        st.error(f"Erro ao buscar atividades: {e}")
        
elif pagina == "📊 Dashboard":
    from components.dashboard import exibir_dashboard
    exibir_dashboard(usuario_id, perfil.get("ftp", 200))
