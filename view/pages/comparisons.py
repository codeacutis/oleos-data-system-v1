import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

from view.queries import queries as q
from view.queries import ( find_child, find_observer, avg_child_items, avg_sleep_by_parents,
                          yes_no_frequency, comportamental_diference, avg_shift, avg_child_items_by_domains)
from view.db import query_execute
import streamlit as st
import plotly.express as px
from datetime import date
import pandas as pd

st.title("Quadro de Comparações", text_alignment="center")

st.header("Comparação Geral entre Crianças por Fase")
fase = st.selectbox(
    'Selecione a fase:', 
    query_execute(q.get("nomes_fases"))
    )

with st.container(key="comparacao_geral"):
    query_shift = query_execute(avg_shift(fase))
    fig = px.bar(query_shift, x='turno', y='media_respostas', color="regular", barmode="group")
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
            key="select_child2"
            )
    with col_center:
        dtframe = pd.concat([query_execute(avg_child_items_by_domains(child1, fase)), query_execute(avg_child_items_by_domains(child2, fase))])
        fig = px.line_polar(
            dtframe, r='media_valor', theta='nome_dominio', color='codigo_crianca'
        )
    
    
    

    
    
    
    