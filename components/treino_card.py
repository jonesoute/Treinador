# components/treino_card.py

import os
import json
import streamlit as st
from datetime import date
from utils.exportador import exportar_treino_para_zwo

def caminho_treinos(usuario_id):
    return os.path.join("data", "usuarios", usuario_id, "treinos_semana.json")

def caminho_feedbacks(usuario_id):
    return os.path.join("data", "usuarios", usuario_id, "feedbacks.json")

def carregar_treinos(usuario_id):
    caminho = caminho_treinos(usuario_id)
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def carregar_feedbacks(usuario_id):
    caminho = caminho_feedbacks(usuario_id)
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def salvar_feedbacks(usuario_id, feedbacks):
    caminho = caminho_feedbacks(usuario_id)
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(feedbacks, f, ensure_ascii=False, indent=4)

def exibir_treinos_semana(usuario_id):
    st.header("📋 Treinos da Semana")
    treinos = carregar_treinos(usuario_id)
    feedbacks = carregar_feedbacks(usuario_id)
    hoje = date.today()

    if not treinos:
        st.info("Nenhum treino foi gerado ainda. Vá para a página inicial e clique em 'Gerar Semana de Treinos'.")
        return

    for data_str in sorted(treinos.keys()):
        dia_data = date.fromisoformat(data_str)
        if dia_data < hoje:
            continue

        st.subheader(f"📅 {dia_data.strftime('%A, %d/%m')}")
        for i, treino in enumerate(treinos[data_str]):
            key = f"{data_str}_{i}"
            with st.container(border=True):
                st.markdown(f"**Modalidade:** {treino['modalidade']}")
                st.markdown(f"**Tipo:** {treino['tipo']}")
                st.markdown(f"**Descrição:** {treino['descricao']}")
                st.markdown(f"**Zonas alvo:** {treino['zona']}")
                st.markdown(f"**Duração:** {treino['tempo']} min")

                # FEEDBACK
                st.markdown("**🗣️ Como você se sentiu após esse treino?**")
                sentimento = st.selectbox(
                    "Selecione uma opção:",
                    ["", "Muito fácil", "Fácil", "Moderado", "Difícil", "Exaustivo"],
                    key=f"fb_{key}"
                )
                if sentimento:
                    feedbacks[key] = {
                        "data": data_str,
                        "modalidade": treino["modalidade"],
                        "tipo": treino["tipo"],
                        "sentimento": sentimento
                    }
                    salvar_feedbacks(usuario_id, feedbacks)
                    st.success("✅ Feedback salvo!")

                # Exportação ZWO
                if treino["modalidade"] == "Ciclismo":
                    if st.button("📤 Exportar como .ZWO", key=f"zwo_{key}"):
                        caminho = exportar_treino_para_zwo(usuario_id, treino)
                        with open(caminho, "r", encoding="utf-8") as f:
                            conteudo = f.read()
                        st.download_button("⬇️ Baixar .ZWO", data=conteudo, file_name=os.path.basename(caminho), mime="application/xml")
                # Exportação TCM
                    if st.button("📤 Exportar como .TCX", key=f"tcx_{key}"):
                        from utils.exportador import exportar_treino_para_tcx
                        caminho = exportar_treino_para_tcx(usuario_id, treino)
                        with open(caminho, "r", encoding="utf-8") as f:
                            conteudo = f.read()
                        st.download_button("⬇️ Baixar .TCX", data=conteudo, file_name=os.path.basename(caminho), mime="application/xml")
