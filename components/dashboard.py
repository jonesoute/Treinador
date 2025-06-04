# components/dashboard.py

import streamlit as st
import matplotlib.pyplot as plt
from utils.analysis import preparar_dataframe_atividades, calcular_cargas

def exibir_dashboard(usuario_id, ftp=200):
    st.header("📊 Dashboard de Carga de Treinamento")

    # Seleção de esporte
    tipo_esporte = st.radio(
        "Qual modalidade deseja visualizar?",
        options=["Ciclismo", "Corrida", "Ambos"],
        horizontal=True
    )

    # Mapear para o tipo do Strava
    tipo_strava = None
    if tipo_esporte == "Ciclismo":
        tipo_strava = "Ride"
    elif tipo_esporte == "Corrida":
        tipo_strava = "Run"

    # Carregar e filtrar atividades
    df = preparar_dataframe_atividades(usuario_id, ftp, tipo=tipo_strava)

    if df.empty:
        st.warning("Nenhuma atividade foi encontrada para essa modalidade.")
        return

    # Cálculo de cargas
    cargas = calcular_cargas(df)

    st.subheader("📌 Indicadores de Carga")
    col1, col2, col3 = st.columns(3)
    col1.metric("Carga Aguda (ATL)", f"{cargas['ATL']} TSS")
    col2.metric("Carga Crônica (CTL)", f"{cargas['CTL']} TSS")
    col3.metric("Forma (TSB)", f"{cargas['TSB']}")

    # Gráfico de TSS diário
    st.subheader("📈 TSS Diário (últimos 42 dias)")
    df_plot = df[df["data"] >= df["data"].max() - pd.Timedelta(days=41)]

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(df_plot["data"], df_plot["tss"], color="#1f77b4")
    ax.set_ylabel("TSS")
    ax.set_xlabel("Data")
    ax.set_title(f"TSS por Dia – {tipo_esporte}")
    ax.grid(True, linestyle="--", alpha=0.5)
    fig.autofmt_xdate()

    st.pyplot(fig)
