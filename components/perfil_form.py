# components/perfil_form.py

import streamlit as st
from datetime import datetime

def exibir_formulario_perfil():
    st.title("🏁 Configuração Inicial - Perfil do Atleta")
    st.markdown("Preencha os dados abaixo para que possamos personalizar seu plano de treinamento:")

    with st.form("form_perfil"):
        nome = st.text_input("Nome completo")
        idade = st.number_input("Idade", min_value=10, max_value=100, step=1)
        sexo = st.selectbox("Sexo", ["Masculino", "Feminino"])
        peso = st.number_input("Peso (kg)", min_value=30.0, max_value=200.0, step=0.1)
        altura = st.number_input("Altura (cm)", min_value=130, max_value=230, step=1)
        ftp = st.number_input("FTP (opcional - em watts)", min_value=50, max_value=600, step=1)

        fc_repouso = st.number_input("Frequência Cardíaca em Repouso (opcional)", min_value=30, max_value=100, step=1)
        fc_maxima = st.number_input("Frequência Cardíaca Máxima (opcional)", min_value=100, max_value=220, step=1)

        experiencia = st.selectbox("Experiência com ciclismo", ["Iniciante", "Intermediário", "Avançado"])
        objetivo = st.text_input("Objetivo principal (ex: ganhar resistência, competir...)")

        referencia_treino = st.radio("Preferência de prescrição de treino", ["Potência", "Frequência Cardíaca"])

        st.markdown("### 🗓️ Dias disponíveis e tempo máximo por dia")
        dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
        dias_disponiveis = st.multiselect("Selecione os dias que pode treinar:", dias_semana)

        horas_disponiveis = {}
        for dia in dias_disponiveis:
            horas_disponiveis[dia] = st.slider(f"{dia} - horas disponíveis", 0.5, 6.0, 1.0, 0.5)

        st.markdown("### ⚙️ Preferências adicionais (opcional)")
        historico_lesoes = st.text_area("Histórico de lesões (se houver)")
        preferencia_treino = st.text_input("Preferência de tipo de treino (intervalado, longos, indoor, etc.)")

        enviado = st.form_submit_button("Salvar Perfil")

    if enviado:
        perfil = {
            "nome": nome,
            "idade": idade,
            "sexo": sexo,
            "peso": peso,
            "altura": altura,
            "ftp": ftp,
            "fc_repouso": fc_repouso,
            "fc_maxima": fc_maxima,
            "experiencia": experiencia,
            "objetivo": objetivo,
            "referencia_treino": referencia_treino,
            "dias_disponiveis": dias_disponiveis,
            "horas_disponiveis": horas_disponiveis,
            "historico_lesoes": historico_lesoes,
            "preferencia_treino": preferencia_treino,
            "data_criacao": datetime.today().strftime("%Y-%m-%d")
        }
        return perfil

    return None

