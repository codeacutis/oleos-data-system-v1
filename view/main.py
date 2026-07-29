import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config
import streamlit as st

pg = st.navigation(
    [st.Page("pages/general.py", title="Visão Geral"), 
     st.Page("pages/children.py", title="Criança"),
     st.Page("pages/comparisons.py", title="Comparações"),
     st.Page("pages/registers.py", title="Registros")], 
    position="top")
pg.run()