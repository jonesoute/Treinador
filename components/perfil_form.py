# components/perfil_form.py

import streamlit as st
from datetime import date
from utils.perfil import salvar_perfil, carregar_perfil

def exibir_formulario_perfil(usuario_id: str):
    st.header("📋 Cadastro / Perfil do Atleta")

    perfil_existente = carregar_perfil(usuario_id)
    novo_perfil = {}

    with st.form("form_perfil"):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("👤 Nome completo", value=perfil_existente.get("nome", ""))
            sexo = st.selectbox("⚧️ Sexo", ["Masculino", "Feminino"], index=["Masculino", "Feminino"].index(perfil_existente.get("sexo", "Masculino")))
            nascimento = st.date_input("📅 Data de nascimento", value=perfil_existente.get("nascimento", date(2000, 1, 1)))
            peso = st.number_input("⚖️ Peso (kg)", min_value=30.0, max_value=200.0, value=perfil_existente.get("peso", 70.0))
            ftp = st.number_input("🚴‍♂️ FTP (opcional)", min_value=0, max_value=600, value=perfil_existente.get("ftp", 200))
        with col2:
            objetivo = st.selectbox("🎯 Objetivo principal", ["Melhorar resistência", "Melhorar velocidade", "Perder peso", "Manter saúde"],
                                    index=["Melhorar resistência", "Melhorar velocidade", "Perder peso", "Manter saúde"].index(perfil_existente.get("objetivo", "Melhorar resistência")))
            modalidade = st.multiselect("🏃‍♂️ Modalidades", ["Ciclismo", "Corrida"], default=perfil_existente.get("modalidades", ["Ciclismo"]))
            preferencia = st.selectbox("📈 Preferência de controle do treino", ["Frequência Cardíaca", "Potência"],
                                       index=["Frequência Cardíaca", "Potência"].index(perfil_existente.get("preferencia", "Frequência Cardíaca")))

        st.markdown("### 🗓️ Dias e Horários disponíveis para treinar")

        dias_semana = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado", "domingo"]
        dias_disponiveis = st.multiselect("Selecione os dias", dias_semana, default=perfil_existente.get("dias_disponiveis", []))

        horas_disponiveis = perfil_existente.get("horas_disponiveis", {})
        horas_resultado = {}

        for dia in dias_disponiveis:
            col = st.columns([1, 5])
            with col[0]:
                st.markdown(f"**{dia.capitalize()}**")
            with col[1]:
                horas_resultado[dia] = st.slider(
                    f"⏱️ Tempo disponível para treino ({dia})", min_value=0.5, max_value=4.0,
                    step=0.5, value=horas_disponiveis.get(dia, 1.0), key=f"hora_{dia}"
                )

        enviado = st.form_submit_button("💾 Salvar perfil")

    if enviado:
        novo_perfil = {
            "nome": nome,
            "sexo": sexo,
            "nascimento": str(nascimento),
            "peso": peso,
            "ftp": ftp,
            "objetivo": objetivo,
            "modalidades": modalidade,
            "preferencia": preferencia,
            "dias_disponiveis": dias_disponiveis,
            "horas_disponiveis": horas_resultado,
            "data_criacao": str(date.today())
        }

        sucesso = salvar_perfil(usuario_id, novo_perfil)

        if sucesso:
            st.success("✅ Perfil salvo com sucesso!")
            if st.button("🔄 OK"):
                st.rerun()
        else:
            st.error("❌ Erro ao salvar o perfil. Tente novamente.")

    return carregar_perfil(usuario_id)
