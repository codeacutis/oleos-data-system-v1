import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config
from view.queries import queries as q
from view.db import query_execute
import streamlit as st
import plotly.express as px
from view.colors import SEQUENCIA_NEUTRA, FASES, VERDE, VERMELHO, AMARELO, LARANJA

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
    if total_children_turn.empty:
        st.info("Nenhum registro encontrado.")
    else:
        fig_turn = px.bar(total_children_turn, x='turno', y='criancas',
                          color='turno', color_discrete_sequence=SEQUENCIA_NEUTRA,
                          labels={'turno': 'Turnos', 'criancas': 'Quantidade de Crianças'})
        st.plotly_chart(fig_turn, key="grafico_turno")

with st.container(key="questionários_respondidos"):
    st.header("Quantidade de questionários respondidos por fase")
    if total_register.empty:
        st.info("Nenhum registro encontrado.")
    else:
        META = 99
        def classificar(v):
            pct = v / META
            if pct >= 1:    return "Na meta"
            if pct >= 0.66: return "Quase na meta"
            if pct >= 0.33: return "Parcialmente"
            return "Muito abaixo"

        total_register["cor"] = total_register["total_registros"].apply(classificar)
        fig_fase = px.bar(
            total_register, x="fase", y="total_registros",
            color="cor",
            color_discrete_map={
                "Na meta":       VERDE,
                "Quase na meta": AMARELO,
                "Parcialmente":  LARANJA,
                "Muito abaixo":  VERMELHO,
            },
            category_orders={"cor": ["Na meta", "Quase na meta", "Parcialmente", "Muito abaixo"]},
            labels={"fase": "Fase", "total_registros": "Questionários Respondidos", "cor": "Status"},
            text="total_registros"
        )
        fig_fase.add_hline(
            y=META, line_dash="dash", line_color=AMARELO,
            annotation_text=f"Meta: {META}",
            annotation_position="top right"
        )
        fig_fase.update_traces(textposition="outside")
        st.plotly_chart(fig_fase, key="grafico_registros_fase")

        col_meta1, col_meta2, col_meta3 = st.columns(3)
        total_geral = int(total_register["total_registros"].sum())
        fases_ok = int((total_register["total_registros"] >= META).sum())
        fases_total = len(total_register)
        col_meta1.metric("Total de Registros", total_geral, delta=f"{total_geral - META * fases_total} vs meta total")
        col_meta2.metric("Fases na Meta", f"{fases_ok}/{fases_total}")
        col_meta3.metric("Meta por Fase", META, help="90 pais (10 dias × 9 crianças) + 9 professores")

with st.container(key="criancas_por_oleo"):
    st.header("Distribuição de Crianças por Óleo")
    if total_children_by_fase.empty:
        st.info("Nenhum registro encontrado.")
    else:
        fig = px.pie(total_children_by_fase, values='criancas', names='fase',
                     color='fase', color_discrete_map=FASES,
                     labels={'criancas': 'Crianças', 'fase': 'Fase'})
        st.plotly_chart(fig)

with st.container(key="linha_tempo"):
    st.header("Linha do Tempo de Registros")
    if register_by_date.empty:
        st.info("Nenhum registro encontrado.")
    else:
        fig = px.line(register_by_date, x="data", y="registros",
                      labels={'data': 'Data', 'registros': 'Registros'},
                      color_discrete_sequence=SEQUENCIA_NEUTRA)
        st.plotly_chart(fig)



    


