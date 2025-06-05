# components/dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px
from utils.analysis import preparar_dataframe_atividades, calcular_cargas
from utils.logger import registrar_erro

def exibir_dashboard(usuario_id, ftp):
    st.header("📊 Painel de Desempenho e Carga")

    try:
        df = preparar_dataframe_atividades(usuario_id, ftp)

        if df.empty:
            st.warning("Nenhuma atividade suficiente encontrada para análise.")
            return

        # Cálculo de métricas de carga
        cargas = calcular_cargas(df)
        st.subheader("📈 Cargas de Treinamento (Últimos 90 dias)")
        col1, col2, col3 = st.columns(3)
        col1.metric("ATL (7d)", cargas["ATL"])
        col2.metric("CTL (42d)", cargas["CTL"])
        col3.metric("TSB", cargas["TSB"], help="CTL - ATL. Reflete fadiga e recuperação.")

        # Gráfico TSS por dia
        st.subheader("📅 TSS Diário")
        fig = px.bar(df, x="data", y="tss", color="tipo", title="TSS por atividade",
                     labels={"data": "Data", "tss": "TSS", "tipo": "Modalidade"})
        st.plotly_chart(fig, use_container_width=True)

        # Gráfico de linha de cargas
        st.subheader("📉 Evolução ATL x CTL")
        df_carga = df.set_index("data")
        fig2 = px.line(df_carga, y=["ATL", "CTL"], title="Carga de Treinamento",
                       labels={"value": "Carga", "variable": "Métrica"})
        st.plotly_chart(fig2, use_container_width=True)

    except Exception as e:
        registrar_erro(f"Erro ao exibir dashboard para '{usuario_id}': {e}")
        st.error("❌ Erro ao gerar o painel. Verifique os dados ou tente novamente.")
