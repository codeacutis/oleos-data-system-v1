import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

from view.queries import queries as q
from view.queries import (adhesion_by_responsible, feeling_by_fase, feeling_evolution,
                          oil_resistance_by_fase, routine_change_by_fase)
from view.db import query_execute
import streamlit as st
import plotly.express as px

st.title("Adesão e Qualidade", text_alignment="center")

# ── 1. Adesão ao protocolo ────────────────────────────────────────────────────

st.header("Adesão ao Protocolo")

df_adhesion = query_execute(adhesion_by_responsible())

if df_adhesion.empty:
    st.info("Nenhum registro encontrado.")
else:
    fig1 = px.bar(
        df_adhesion,
        x="total_registros",
        y="responsavel",
        color="fase",
        orientation="h",
        barmode="group",
        labels={"total_registros": "Registros", "responsavel": "Responsável", "fase": "Fase"},
    )
    fig1.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig1, key="grafico_adesao")

# ── 2. Sentimento dos responsáveis ────────────────────────────────────────────

st.header("Sentimento dos Responsáveis")

col_left, col_right = st.columns([2, 1], gap="large")

with col_left:
    st.subheader("Evolução por Fase")
    df_feeling_evo = query_execute(feeling_evolution())
    if df_feeling_evo.empty:
        st.info("Nenhum registro encontrado.")
    else:
        fig2 = px.bar(
            df_feeling_evo,
            x="fase",
            y="frequencia",
            color="sentimento",
            barmode="stack",
            labels={"frequencia": "Frequência", "fase": "Fase", "sentimento": "Sentimento"},
        )
        st.plotly_chart(fig2, key="grafico_sentimento_evolucao")

with col_right:
    st.subheader("Distribuição por Fase")
    fase_sentimento = st.selectbox(
        "Selecione a fase:",
        query_execute(q.get("nomes_fases")),
        key="select_fase_sentimento"
    )
    df_feeling = query_execute(feeling_by_fase(fase_sentimento))
    if df_feeling.empty:
        st.info("Nenhum registro encontrado.")
    else:
        fig3 = px.pie(
            df_feeling,
            names="sentimento",
            values="frequencia",
            hole=0.45,
        )
        fig3.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig3, key="grafico_sentimento_donut")

# ── 3. Resistência ao óleo ────────────────────────────────────────────────────

st.header("Resistência ao Óleo")

df_resistance = query_execute(oil_resistance_by_fase())

if df_resistance.empty:
    st.info("Nenhum registro encontrado.")
else:
    fig4 = px.bar(
        df_resistance,
        x="fase",
        y="frequencia",
        labels={"frequencia": "Ocorrências", "fase": "Fase"},
    )
    st.plotly_chart(fig4, key="grafico_resistencia")

# ── 4. Mudanças na rotina ─────────────────────────────────────────────────────

st.header("Mudanças na Rotina")

df_routine = query_execute(routine_change_by_fase())

if df_routine.empty:
    st.info("Nenhum registro encontrado.")
else:
    fig5 = px.bar(
        df_routine,
        x="fase",
        y="frequencia",
        labels={"frequencia": "Ocorrências", "fase": "Fase"},
    )
    st.plotly_chart(fig5, key="grafico_rotina")
