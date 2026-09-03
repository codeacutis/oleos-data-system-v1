import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config
from view.queries import queries as q
from view.queries import ( find_child, find_observer, avg_child_items, 
                          avg_sleep_by_parents, yes_no_frequency, comportamental_diference )
from view.db import query_execute
import streamlit as st
import plotly.express as px
from datetime import date
import pandas as pd
from view.colors import FASES, AZUL, VERDE, VERMELHO, EVENTOS_ADVERSOS

st.title("Análise por Criança", text_alignment='center')

option = st.selectbox(
    'Selecione uma criança:', 
    query_execute(q.get("codigos_criancas"))
    )

child = query_execute(*find_child(option))
observer = query_execute(*find_observer(int(child['id_crianca'].values[0])))
teacher = observer[observer['tipo'] == 'PROFESSOR']['codigo'].values[0]
parent = observer[observer['tipo'] == 'RESPONSAVEL']['codigo'].values[0]

today = date.today()
databruta = pd.to_datetime((child['data_nascimento'].values[0])).date()
idade = (
today.year
- databruta.year
- (
    (today.month, today.day)
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
    query_item = query_execute(*avg_child_items(option))
    if query_item.empty:
        st.info("Nenhum registro encontrado.")
    else:
        fig = px.bar(query_item, x='item', y='media_valor', color="fase", barmode="group",
                     color_discrete_map=FASES,
                     labels={'item': 'Item', 'media_valor': 'Média', 'fase': 'Fase'})
        st.plotly_chart(fig, key="grafico_linhaBaseXoleos")
    
#comparação entre ambientes
with st.container(key="ambientes"):
    st.header("Média por Item - Ambiente Domiciliar")
    
    st.subheader("Evolução do Sono")
    query_sleep = query_execute(*avg_sleep_by_parents(option))
    if query_sleep.empty:
        st.info("Nenhum registro encontrado.")
    else:
        fig2 = px.line(query_sleep, x='fase', y='media_valor',
                       color_discrete_sequence=[AZUL],
                       labels={'fase': 'Fase', 'media_valor': 'Média de Sono (h)'})
        st.plotly_chart(fig2, key="grafico_sono")
    
    st.subheader("Frequência de Eventos Adversos")
    query_adversities = query_execute(*yes_no_frequency(option))
    if query_adversities.empty:
        st.info("Nenhum registro encontrado.")
    else:
        fig_adv = px.bar(query_adversities, x='fase', y='frequencia', color='descricao',
                         barmode='group', color_discrete_map=EVENTOS_ADVERSOS,
                         labels={'fase': 'Fase', 'frequencia': 'Frequência', 'descricao': 'Evento'})
        st.plotly_chart(fig_adv, key="grafico_eventos_adversos")
    
    st.subheader("Comportamento ao ir e voltar da escola")
    fase = st.selectbox("Fase", query_execute(q.get("nomes_fases")), key="select_fase_comportamental")
    query_comportamental = query_execute(*comportamental_diference(option, fase))
    if query_comportamental.empty:
        st.info("Nenhum registro encontrado.")
    else:
        st.dataframe(query_comportamental, width="stretch", hide_index=True)
    
    
    


