# components/calendar.py

import streamlit as st
import json
import os
from datetime import date, timedelta

def caminho_provas(usuario_id):
    return os.path.join("data", "usuarios", usuario_id, "provas.json")

def carregar_provas(usuario_id):
    caminho = caminho_provas(usuario_id)
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_provas(usuario_id, provas):
    caminho = caminho_provas(usuario_id)
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(provas, f, ensure_ascii=False, indent=4)

def exibir_calendario_provas(usuario_id):
    st.header("📅 Calendário de Competições")
    
    provas = carregar_provas(usuario_id)

    with st.expander("➕ Adicionar nova competição"):
        with st.form("form_prova"):
            nome_evento = st.text_input("Nome do Evento")
            tipo = st.selectbox("Modalidade", ["Ciclismo", "Corrida"])
            data_inicio = st.date_input("Data de Início", min_value=date.today())
            data_fim = st.date_input("Data de Término", min_value=data_inicio)
            duracao = (data_fim - data_inicio).days + 1
            distancia = st.number_input("Distância total (km)", min_value=1.0)
            altimetria = st.number_input("Altimetria acumulada (opcional - metros)", min_value=0.0, value=0.0)

            enviar = st.form_submit_button("Salvar Competição")

        if enviar:
            nova = {
                "nome": nome_evento,
                "tipo": tipo,
                "data_inicio": str(data_inicio),
                "data_fim": str(data_fim),
                "dias": duracao,
                "distancia_km": distancia,
                "altimetria_m": altimetria
            }
            provas.append(nova)
            salvar_provas(usuario_id, provas)
            st.success("✅ Competição adicionada com sucesso!")

    if provas:
        st.subheader("📍 Competições Registradas")
        for prova in provas:
            st.markdown(
                f"- **{prova['nome']}** ({prova['tipo']}) | "
                f"{prova['data_inicio']} a {prova['data_fim']} | "
                f"{prova['distancia_km']} km | "
                f"{int(prova['altimetria_m'])} m alt."
            )
    else:
        st.info("Nenhuma competição registrada ainda.")

