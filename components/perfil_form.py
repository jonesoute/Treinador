import streamlit as st
from datetime import date

def exibir_formulario_perfil(usuario_id):
    st.header("📝 Preencha seu perfil inicial")

    with st.form("form_perfil", clear_on_submit=False):
        nome = st.text_input("Nome completo")
        idade = st.number_input("Idade", min_value=12, max_value=100, value=30)
        sexo = st.radio("Sexo", ["Masculino", "Feminino"])
        peso = st.number_input("Peso (kg)", min_value=30.0, max_value=150.0, value=70.0)
        altura = st.number_input("Altura (cm)", min_value=130, max_value=210, value=175)
        ftp = st.number_input("FTP estimado (W)", min_value=100, max_value=500, value=200)
        modalidades = st.multiselect("Modalidades", ["Ciclismo", "Corrida"], default=["Ciclismo"])
        preferencia = st.radio("Preferência de treino", ["Frequência Cardíaca", "Potência"])

        st.markdown("**📆 Disponibilidade Semanal**")
        dias_semana = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado", "domingo"]
        dias_disponiveis = st.multiselect("Dias disponíveis para treinar:", dias_semana)
        horas_disponiveis = {}
        for dia in dias_disponiveis:
            horas = st.slider(f"{dia.capitalize()}: Quantas horas?", 0.5, 5.0, 1.0, 0.5)
            horas_disponiveis[dia] = horas

        enviar = st.form_submit_button("Salvar Perfil")

        if enviar:
            perfil = {
                "nome": nome,
                "idade": idade,
                "sexo": sexo,
                "peso": peso,
                "altura": altura,
                "ftp": ftp,
                "modalidades": modalidades,
                "preferencia": preferencia,
                "dias_disponiveis": dias_disponiveis,
                "horas_disponiveis": horas_disponiveis,
                "data_criacao": date.today().isoformat()
            }

            # Armazenar temporariamente na sessão
            st.session_state["perfil_temp"] = perfil
            st.success("✅ Perfil salvo com sucesso!")

            # Mostra botão para recarregar app
            if st.button("✅ OK"):
                st.experimental_rerun()

            return perfil  # <- Só retorna após o botão "OK"
