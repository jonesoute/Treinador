# components/login.py

import streamlit as st
from supabase import create_client, Client
from utils.db_supabase import supabase


def exibir_login():
    st.title("🔐 Login do Atleta")
    st.markdown("Acesse sua conta com seu e-mail e senha cadastrados.")

    with st.form("login_form"):
        email = st.text_input("E-mail")
        senha = st.text_input("Senha", type="password")
        login = st.form_submit_button("Entrar")
        primeiro_acesso = st.form_submit_button("🔓 Primeiro Acesso")

    if primeiro_acesso:
        st.session_state["primeiro_acesso"] = True
        st.experimental_rerun()

    if login:
        if not email or not senha:
            st.warning("Preencha todos os campos para entrar.")
            return None

        try:
            supabase: Client = get_supabase_client()
            resultado = supabase.auth.sign_in_with_password({
                "email": email,
                "password": senha
            })

            usuario = resultado.user
            if usuario:
                st.success("Login realizado com sucesso!")
                st.session_state["usuario_id"] = usuario.id
                st.session_state["usuario_email"] = email
                st.experimental_rerun()
            else:
                st.error("E-mail ou senha inválidos.")

        except Exception as e:
            st.error(f"Erro ao tentar login: {e}")
            return None
