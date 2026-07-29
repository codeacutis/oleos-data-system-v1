import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config
from view.queries import queries as q
from view.queries import (find_child, find_observer, avg_child_items, avg_sleep_by_parents)
from view.db import query_execute
import streamlit as st
import plotly.express as px
from datetime import date
import pandas as pd

st.title("Análise por Criança", text_alignment='center')

option = st.selectbox(
    'Selecione uma criança:', 
    query_execute(q.get("codigos_criancas"))
    )

child = query_execute(find_child(option))
observer = query_execute(find_observer(child['id_crianca'].values[0]))
teacher = observer[observer['tipo'] == 'PROFESSOR']['nome'].values[0]
parent = observer[observer['tipo'] == 'RESPONSAVEL']['nome'].values[0]

hoje = date.today()
databruta = pd.to_datetime((child['data_nascimento'].values[0])).date()
idade = (
hoje.year
- databruta.year
- (
    (hoje.month, hoje.day)
    < (databruta.month, databruta.day)
))

#informações da criança
with st.container(key="informaçoes"):
    st.header("Informações da Criança")
    column1, column2 = st.columns(2)
    with column1:
        st.write(f"Código: {child['codigo'].values[0]}")
        st.write(f"Idade: {idade} anos")
        st.write(f"Turno: {(child['turno'].values[0]).title()}")
    with column2:
        st.write(f"Regular: {(child['regular'].values[0]).title()}")
        st.write(f"Professor: {teacher}")
        st.write(f"Responsável: {parent}")
        
#comparação linha de base x óleo
with st.container(key="comparacao"):
    st.header("Média por Item - Linha de Base x Óleo")
    query_item = query_execute(avg_child_items(option))
    fig = px.bar(query_item, x='item', y='media_valor', color="fase", barmode="group")
    st.plotly_chart(fig, key="grafico_linhaBaseXoleos")
    
#comparação entre ambientes
with st.container(key="ambientes"):
    st.header("Média por Item - Ambiente Domiciliar")
    
    #evolução do sono ao longo das fases
    st.subheader("Evolução do Sono")
    query_sleep = query_execute(avg_sleep_by_parents(option))
    fig2 = px.line(query_sleep, x='fase', y='media_valor')
    st.plotly_chart(fig2, key="grafico_sono")
    
    


