# components/treino_editor.py

import os
import json
import streamlit as st
from datetime import date

TREINOS_PATH = "data/usuarios/{}/treinos_semana.json"
EDICOES_PATH = "data/usuarios/{}/edicoes.json"


def carregar_treinos(usuario_id):
    caminho = TREINOS_PATH.format(usuario_id)
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def salvar_treinos(usuario_id, treinos):
    caminho = TREINOS_PATH.format(usuario_id)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(treinos, f, ensure_ascii=False, indent=4)


def salvar_edicao(usuario_id, tipo, data_original, nova_data, treino):
    caminho = EDICOES_PATH.format(usuario_id)
    edicoes = []
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            edicoes = json.load(f)

    edicoes.append({
        "tipo": tipo,
        "data_original": data_original,
        "nova_data": nova_data,
        "treino": treino
    })

    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(edicoes, f, ensure_ascii=False, indent=4)


def treino_editor(usuario_id):
    st.header("✏️ Editor de Treinos Semanais")
    treinos = carregar_treinos(usuario_id)
    dias = sorted([d for d in treinos if d != "_mensagem"])

    if "_mensagem" in treinos:
        st.warning(treinos["_mensagem"])

    for dia in dias:
        st.subheader(f"📅 {dia}")
        novos_treinos = []

        for i, treino in enumerate(treinos[dia]):
            st.markdown(f"**{treino['modalidade']} – {treino['tipo']}**")
            st.markdown(f"{treino['descricao']}")

            col1, col2, col3 = st.columns([2, 2, 2])
            with col1:
                nova_data = st.date_input("Mover para outro dia", date.fromisoformat(dia), key=f"mover_{dia}_{i}")
                if nova_data.isoformat() != dia:
                    salvar_edicao(usuario_id, "mover", dia, nova_data.isoformat(), treino)
                    if nova_data.isoformat() not in treinos:
                        treinos[nova_data.isoformat()] = []
                    treinos[nova_data.isoformat()].append({**treino, "_editado": True})
                    st.success(f"Treino movido para {nova_data}")
                    continue  # Não duplicar na exibição

            with col2:
                if st.button("❌ Excluir treino", key=f"excluir_{dia}_{i}"):
                    salvar_edicao(usuario_id, "excluir", dia, None, treino)
                    st.warning("Treino excluído")
                    continue

            with col3:
                if treino.get("_editado"):
                    st.info("🔄 Treino editado manualmente")

            novos_treinos.append(treino)

        treinos[dia] = novos_treinos

    salvar_treinos(usuario_id, treinos)
    st.success("✅ Edições salvas com sucesso")

    # Restaurar plano original
    if st.button("🔁 Restaurar plano original da semana"):
        os.remove(TREINOS_PATH.format(usuario_id))
        if os.path.exists(EDICOES_PATH.format(usuario_id)):
            os.remove(EDICOES_PATH.format(usuario_id))
        st.experimental_rerun()
