# components/calendar.py

import os
import json
import streamlit as st
from datetime import datetime, timedelta
from utils.logger import registrar_erro

def caminho_provas(usuario_id):
    return os.path.join("data", "usuarios", usuario_id, "provas.json")

def carregar_provas(usuario_id):
    try:
        caminho = caminho_provas(usuario_id)
        if os.path.exists(caminho):
            with open(caminho, "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    except Exception as e:
        registrar_erro(f"Erro ao carregar provas do usuário '{usuario_id}': {e}")
        return []

def salvar_provas(usuario_id, provas):
    try:
        caminho = caminho_provas(usuario_id)
        os.makedirs(os.path.dirname(caminho), exist_ok=True)
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(provas, f, ensure_ascii=False, indent=4)
    except Exception as e:
        registrar_erro(f"Erro ao salvar provas do usuário '{usuario_id}': {e}")

def exibir_calendario_provas(usuario_id):
    st.header("📆 Calendário de Competições")

    provas = carregar_provas(usuario_id)

    with st.expander("➕ Adicionar nova competição"):
        nome = st.text_input("Nome da competição")
        tipo = st.selectbox("Modalidade", ["Ciclismo", "Corrida"])
        data_inicio = st.date_input("Data de início", value=datetime.today())
        data_fim = st.date_input("Data de término", value=data_inicio)
        distancia_km = st.number_input("Distância total (km)", min_value=1.0, step=1.0)
        altimetria_m = st.number_input("Altimetria acumulada (m)", min_value=0.0, step=10.0)

        if st.button("➕ Salvar competição"):
            nova_prova = {
                "nome": nome,
                "tipo": tipo,
                "data_inicio": data_inicio.isoformat(),
                "data_fim": data_fim.isoformat(),
                "distancia_km": distancia_km,
                "altimetria_m": altimetria_m
            }
            provas.append(nova_prova)
            salvar_provas(usuario_id, provas)
            st.success("✅ Competição salva com sucesso!")
            st.experimental_rerun()

    if provas:
        st.subheader("📋 Competições cadastradas")
        for i, prova in enumerate(provas):
            with st.container(border=True):
                st.markdown(f"**🏁 {prova['nome']}**")
                st.markdown(f"📅 {prova['data_inicio']} até {prova['data_fim']}")
                st.markdown(f"🚴 Modalidade: {prova['tipo']}")
                st.markdown(f"📏 Distância: {prova['distancia_km']} km")
                st.markdown(f"⛰️ Altimetria: {prova['altimetria_m']} m")
                if st.button("🗑️ Excluir", key=f"del_{i}"):
                    provas.pop(i)
                    salvar_provas(usuario_id, provas)
                    st.success("🗑️ Competição excluída.")
                    st.experimental_rerun()
    else:
        st.info("Nenhuma competição cadastrada ainda.")
