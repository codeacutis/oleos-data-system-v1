import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config
from view.queries import queries as q
from view.db import query_execute
import streamlit as st
import plotly.express as px

#get das queries
total_children = query_execute(q.get('total_criancas_cadastradas'))
total_parents = query_execute(q.get('total_pais'))
total_teacher = query_execute(q.get('total_professores'))
total_register = query_execute(q.get('total_registros_por_fase'))
total_children_turn = query_execute(q.get('total_criancas_turno')) 
total_children_by_fase = query_execute(q.get('criancas_por_fase'))
register_by_date = query_execute(q.get('registros_por_data'))

#estruturação da tela
st.title("Visão Geral", text_alignment="center")

with st.container(key="metricas"):
    st.header("Métricas")
    column1, column2, column3 = st.columns(3)
    column1.metric(label="Total de Crianças Cadastradas", value=total_children.iloc[0], border=True)
    column2.metric(label="Total de Responsáveis", value=total_parents.iloc[0], border=True)
    column3.metric(label="Total de Professores", value=total_teacher.iloc[0], border=True)

with st.container(key="criancas_por_turno"):
    st.header("Distribuição de Crianças por Turno")
    st.bar_chart(total_children_turn, x='turno', y='criancas', x_label="Turnos", y_label="Quantidade de Crianças")

with st.container(key="questionários_respondidos"):
    st.header("Quantidade de questionários respondidos por fase")
    st.bar_chart(total_register, x='fase', y='total_registros', x_label="Fase", y_label="Questionários Respondidos", horizontal=True)

with st.container(key="criancas_por_oleo"):
    st.header("Distribuição de Crianças por Óleo")
    fig = px.pie(total_children_by_fase, values='criancas', names='fase')
    st.plotly_chart(fig)

with st.container(key="linha_tempo"):
    st.header("Linha do Tempo de Registros")
    fig = px.line(register_by_date, x="data", y="registros")
    st.plotly_chart(fig)



    


