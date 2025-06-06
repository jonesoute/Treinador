# components/perfil_form.py

import streamlit as st
from datetime import date

def exibir_formulario_perfil(usuario_id):
    st.subheader("📋 Preencha seu perfil de atleta")

    nome = st.text_input("Nome completo")
    sexo = st.radio("Sexo", ["Masculino", "Feminino"])
    idade = st.number_input("Idade", min_value=10, max_value=90, value=30)
    peso = st.number_input("Peso (kg)", min_value=30.0, max_value=150.0, value=70.0)
    altura = st.number_input("Altura (cm)", min_value=130, max_value=220, value=175)
    ftp = st.number_input("FTP estimado (opcional)", min_value=100, max_value=500, value=200)

    modalidades = st.multiselect("Modalidades praticadas", ["Ciclismo", "Corrida"], default=["Ciclismo"])
    preferencia = st.radio("Preferência de treino", ["Frequência Cardíaca", "Potência"])

    st.markdown("### 🗓️ Disponibilidade semanal")
    dias = st.multiselect("Quais dias você pode treinar?", ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado", "domingo"])
    horas = {}
    for dia in dias:
        horas[dia] = st.slider(f"⏱️ Tempo disponível na {dia}", 0.5, 6.0, 1.0, step=0.5)

    if st.button("💾 Salvar Perfil"):
        return {
            "nome": nome,
            "sexo": sexo,
            "idade": idade,
            "peso": peso,
            "altura": altura,
            "ftp": ftp,
            "modalidades": modalidades,
            "preferencia_treino": preferencia,
            "dias_disponiveis": dias,
            "horas_disponiveis": horas,
            "data_criacao": date.today().isoformat()
        }

    return None
