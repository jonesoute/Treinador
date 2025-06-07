# components/perfil_form.py

import streamlit as st
from datetime import date
from utils.db_supabase import salvar_perfil, carregar_perfil

def exibir_formulario_perfil(usuario_id):
    st.header("📝 Configurar Perfil do Atleta")

    perfil_existente = carregar_perfil(usuario_id)

    if perfil_existente:
        st.success("✅ Perfil já existente carregado.")
        return perfil_existente

    with st.form("perfil_formulario"):
        nome = st.text_input("Nome completo")
        email = st.text_input("E-mail")
        sexo = st.selectbox("Sexo", ["Masculino", "Feminino"])
        data_nascimento = st.date_input("Data de nascimento", min_value=date(1920, 1, 1), max_value=date.today())
        peso = st.number_input("Peso (kg)", min_value=30.0, max_value=200.0, step=0.1)
        altura = st.number_input("Altura (cm)", min_value=100, max_value=230)
        ftp = st.number_input("FTP (opcional, watts)", min_value=0)
        modalidades = st.multiselect("Modalidades praticadas", ["Ciclismo", "Corrida"], default=["Ciclismo"])

        dias_semana = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado", "domingo"]
        dias_disponiveis = st.multiselect("Dias disponíveis para treinar", dias_semana)

        enviar = st.form_submit_button("Salvar Perfil")

    if enviar:
        hoje = date.today()
        horas_disponiveis = {}
        for dia in dias_disponiveis:
            horas = st.slider(f"⏱️ Quantas horas você pode treinar na {dia}?", 0.5, 6.0, 1.0, 0.5, key=dia)
            horas_disponiveis[dia] = horas

        perfil = {
            "id": usuario_id,
            "nome": nome,
            "email": email,
            "sexo": sexo,
            "data_nascimento": str(data_nascimento),
            "peso": peso,
            "altura": altura,
            "ftp": ftp,
            "modalidades": modalidades,
            "dias_disponiveis": dias_disponiveis,
            "horas_disponiveis": horas_disponiveis,
            "data_criacao": str(hoje)
        }

        salvar_perfil(perfil)

        st.success("✅ Perfil salvo com sucesso!")
        st.button("🔄 OK para atualizar", on_click=st.rerun)

        return perfil
