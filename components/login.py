# components/login.py

import streamlit as st
from utils.perfil import verificar_login

def exibir_login():
    st.sidebar.header("👤 Identificação do Atleta")
    with st.sidebar.form("login_form"):
        email = st.text_input("E-mail")
        senha = st.text_input("Senha", type="password")
        submit = st.form_submit_button("Entrar")

        if submit:
            if verificar_login(email, senha):
                st.session_state["usuario_id"] = email
                st.rerun()
            else:
                st.error("E-mail ou senha inválidos.")

    # Se o botão for clicado, redireciona para cadastro (primeiro acesso)
    if st.sidebar.button("🚀 Primeiro Acesso"):
        st.session_state["primeiro_acesso"] = True
        st.rerun()

    return st.session_state.get("usuario_id")
