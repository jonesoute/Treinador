# components/perfil_form.py

import streamlit as st
from datetime import date, datetime
from utils.db_supabase import salvar_perfil, carregar_perfil

def exibir_formulario_perfil(usuario_id):
    st.header("📝 Cadastro do Atleta")

    perfil_existente = carregar_perfil(usuario_id)
    preenchido = bool(perfil_existente)

    with st.form("form_perfil"):
        nome = st.text_input("Nome completo", value=perfil_existente.get("nome", ""))
        data_nascimento = st.date_input("Data de nascimento", value=perfil_existente.get("data_nascimento", date(2000, 1, 1)))
        sexo = st.selectbox("Sexo", ["Masculino", "Feminino", "Outro"], index=["Masculino", "Feminino", "Outro"].index(perfil_existente.get("sexo", "Masculino")))
        peso = st.number_input("Peso (kg)", min_value=30.0, max_value=200.0, value=float(perfil_existente.get("peso", 70)))
        ftp = st.number_input("FTP (se souber)", min_value=100, max_value=500, value=int(perfil_existente.get("ftp", 200)))
        modalidades = st.multiselect("Modalidades praticadas", ["Ciclismo", "Corrida"], default=perfil_existente.get("modalidades", ["Ciclismo"]))
        preferencia = st.radio("Preferência de controle do treino", ["Frequência Cardíaca", "Potência"], index=["Frequência Cardíaca", "Potência"].index(perfil_existente.get("preferencia", "Frequência Cardíaca")))

        dias_semana = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado", "domingo"]
        dias_disponiveis = st.multiselect("Dias disponíveis para treinar", dias_semana, default=perfil_existente.get("dias_disponiveis", []))

        horas_disponiveis = {}
        if dias_disponiveis:
            st.markdown("### ⏱️ Horas disponíveis por dia")
            for dia in dias_disponiveis:
                horas_disponiveis[dia] = st.slider(
                    f"{dia.capitalize()}", 0.5, 4.0,
                    value=float(perfil_existente.get("horas_disponiveis", {}).get(dia, 1.0)),
                    step=0.5
                )

        submit = st.form_submit_button("💾 Salvar Perfil")

    if submit:
        idade = calcular_idade(data_nascimento)
        perfil = {
            "nome": nome,
            "data_nascimento": str(data_nascimento),
            "idade": idade,
            "sexo": sexo,
            "peso": peso,
            "ftp": ftp,
            "modalidades": modalidades,
            "preferencia": preferencia,
            "dias_disponiveis": dias_disponiveis,
            "horas_disponiveis": horas_disponiveis,
            "data_criacao": perfil_existente.get("data_criacao", str(date.today()))
        }

        sucesso = salvar_perfil(usuario_id, perfil)
        if sucesso:
            st.success("✅ Perfil salvo com sucesso!")
            st.rerun()
        else:
            st.error("Erro ao salvar o perfil. Tente novamente.")

    return perfil_existente

def calcular_idade(data_nascimento):
    hoje = date.today()
    return hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))
