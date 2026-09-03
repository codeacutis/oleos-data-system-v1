import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

from view.queries import queries as q
from view.queries import ( find_child, find_observer, avg_child_items, avg_sleep_by_parents,
                          yes_no_frequency, comportamental_diference, avg_shift, avg_child_items_by_domains,
                          avg_domains_by_oil, avg_sleep_by_oil, yes_no_frequency_by_oil, comportamental_by_oil,
                          avg_baseline_vs_intervention, sleep_baseline_vs_intervention,
                          avg_by_environment, avg_sleep_by_parents_by_fase, yes_no_frequency_by_fase)
from view.db import query_execute
import streamlit as st
import plotly.express as px
from datetime import date
import pandas as pd
from view.colors import (FASES, PERIODOS, SENTIMENTOS, AMBIENTES, COMPORTAMENTO,
                         SEQUENCIA_NEUTRA, SEQUENCIA_DOMINIOS, SEQUENCIA_OLEOS,
                         VERDE, VERMELHO, AZUL, AMARELO, EVENTOS_ADVERSOS)

st.title("Quadro de Comparações", text_alignment="center")

st.header("Comparação Geral entre Crianças por Fase")
fase = st.selectbox(
    'Selecione a fase:', 
    query_execute(q.get("nomes_fases"))
    )

with st.container(key="comparacao_geral"):
    query_shift = query_execute(*avg_shift(fase))
    if query_shift.empty:
        st.info("Nenhum registro encontrado.")
    else:
        fig = px.bar(query_shift, x='turno', y='media_respostas', color="regular", barmode="group",
                     color_discrete_sequence=SEQUENCIA_NEUTRA,
                     labels={'turno': 'Turno', 'media_respostas': 'Média', 'regular': 'Regular'})
        st.plotly_chart(fig, key="grafico_comparacao_turnos_fase")
    
    st.header("Comparação Individual entre Crianças")
    col_left, col_center, col_right = st.columns([1, 2, 1], gap="large")  
    with col_left:
        child1 = st.selectbox(
            'Selecione uma criança:',
            query_execute(q.get("codigos_criancas")),
            key="select_child1"
            )
    with col_right:
        child2 = st.selectbox(
            'Selecione uma criança:',
            query_execute(q.get("codigos_criancas")),
            index=1,
            key="select_child2"
            )
    with col_center:
        dtframe = pd.concat([query_execute(*avg_child_items_by_domains(child1, fase)), query_execute(*avg_child_items_by_domains(child2, fase))])
        if dtframe.empty:
            st.info("Nenhum registro encontrado.")
        else:
            fig = px.line_polar(dtframe, r='media_valor', theta='nome_dominio', color='codigo_crianca',
                                color_discrete_sequence=[AZUL, AMARELO],
                                labels={'media_valor': 'Média', 'nome_dominio': 'Domínio', 'codigo_crianca': 'Criança'})
            st.plotly_chart(fig, key="grafico_radar")
    
st.header("Comparação entre Óleos Essenciais")

with st.container(key="scores_por_oleo"):
    st.subheader("Scores por Domínio")
    df_domains = query_execute(avg_domains_by_oil())
    if df_domains.empty:
        st.info("Nenhum registro encontrado.")
    else:
        fig = px.bar(df_domains, x='oleo', y='media_valor', color='dominio',
                     color_discrete_sequence=SEQUENCIA_DOMINIOS,
                     labels={'oleo': 'Óleo', 'media_valor': 'Média', 'dominio': 'Domínio'})
        st.plotly_chart(fig, key="grafico_dominios_oleo")

with st.container(key="dados_pais_oleo"):
    st.subheader("Dados dos Pais por Óleo")
    
    col1, col2 = st.columns([1, 2], gap="medium")
    
    with col1:
        st.write("**Média de Sono**")
        df_sleep = query_execute(avg_sleep_by_oil())
        if df_sleep.empty:
            st.info("Nenhum registro encontrado.")
        else:
            fig2 = px.bar(df_sleep, x='oleo', y='media_sono', color='oleo',
                          color_discrete_sequence=SEQUENCIA_OLEOS,
                          labels={'oleo': 'Óleo', 'media_sono': 'Média de Sono (h)'})
            st.plotly_chart(fig2, key="grafico_sono_oleo")

    with col2:
        st.write("**Comportamento**")
        df_comp = query_execute(comportamental_by_oil())
        if df_comp.empty:
            st.info("Nenhum registro encontrado.")
        else:
            fig4 = px.bar(df_comp, x='oleo', y='frequencia', color='resposta', barmode='group',
                          color_discrete_map=COMPORTAMENTO,
                          facet_row='pergunta',
                          labels={'oleo': 'Óleo', 'frequencia': 'Frequência', 'resposta': 'Resposta', 'pergunta': 'Pergunta'})
            st.plotly_chart(fig4, key="grafico_comportamento_oleo")
    
    st.write("**Eventos Adversos**")
    df_yesno = query_execute(yes_no_frequency_by_oil())
    if df_yesno.empty:
        st.info("Nenhum registro encontrado.")
    else:
        fig3 = px.bar(df_yesno, x='oleo', y='frequencia', color='pergunta', barmode='group',
                        color_discrete_map=EVENTOS_ADVERSOS,
                        labels={'oleo': 'Óleo', 'frequencia': 'Frequência', 'pergunta': 'Pergunta'})
        st.plotly_chart(fig3, key="grafico_eventos_oleo")

st.header("Linha de Base vs Intervenção")

with st.container(key="baseline_vs_intervention"):
    col1, col2 = st.columns(2)

    with col1:
        st.write("**Scores por Domínio (Professores)**")
        df_bv = query_execute(avg_baseline_vs_intervention())
        if df_bv.empty:
            st.info("Nenhum registro encontrado.")
        else:
            fig5 = px.bar(df_bv, x='dominio', y='media_valor', color='periodo', barmode='group',
                          color_discrete_map=PERIODOS,
                          labels={'dominio': 'Domínio', 'media_valor': 'Média', 'periodo': 'Período'})
            st.plotly_chart(fig5, key="grafico_baseline_dominios")

    with col2:
        st.write("**Média de Sono (Responsáveis)**")
        df_sleep_bv = query_execute(sleep_baseline_vs_intervention())
        if df_sleep_bv.empty:
            st.info("Nenhum registro encontrado.")
        else:
            fig6 = px.bar(df_sleep_bv, x='periodo', y='media_sono', color='periodo',
                          color_discrete_map=PERIODOS,
                          labels={'periodo': 'Período', 'media_sono': 'Média de Sono (h)'})
            st.plotly_chart(fig6, key="grafico_baseline_sono")

st.header("Comparação entre Ambientes")

fase_amb = st.selectbox(
    'Selecione a fase:',
    query_execute(q.get("nomes_fases")),
    key="select_fase_ambiente"
)

with st.container(key="comparacao_ambientes"):
    st.subheader("Ambiente Escolar — Scores por Domínio (Professores)")
    df_env = query_execute(*avg_by_environment(fase_amb))
    if df_env.empty:
        st.info("Nenhum registro encontrado.")
    else:
        fig7 = px.bar(df_env, x='dominio', y='media_valor', color='dominio',
                      color_discrete_sequence=SEQUENCIA_DOMINIOS,
                      labels={'dominio': 'Domínio', 'media_valor': 'Média'})
        st.plotly_chart(fig7, key="grafico_ambiente_dominios")

    st.subheader("Ambiente Domiciliar — Dados dos Responsáveis")
    col1, col2 = st.columns(2)

    with col1:
        st.write("**Média de Sono**")
        df_sleep_amb = query_execute(*avg_sleep_by_parents_by_fase(fase_amb))
        if df_sleep_amb.empty:
            st.info("Nenhum registro encontrado.")
        else:
            fig8 = px.bar(df_sleep_amb, x='fase', y='media_valor', color='fase',
                          color_discrete_map=FASES,
                          labels={'fase': 'Fase', 'media_valor': 'Média de Sono (h)'})
            st.plotly_chart(fig8, key="grafico_ambiente_sono")

    with col2:
        st.write("**Eventos Adversos**")
        df_yesno_amb = query_execute(*yes_no_frequency_by_fase(fase_amb))
        if df_yesno_amb.empty:
            st.info("Nenhum registro encontrado.")
        else:
            fig9 = px.bar(df_yesno_amb, x='descricao', y='frequencia', color='descricao',
                          color_discrete_map=EVENTOS_ADVERSOS,
                          labels={'descricao': 'Evento', 'frequencia': 'Frequência'})
            st.plotly_chart(fig9, key="grafico_ambiente_eventos")