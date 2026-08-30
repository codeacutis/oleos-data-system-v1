import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config
import streamlit as st
import streamlit_authenticator as stauth
import mysql.connector
from view.db import query_execute
from view.queries import queries as q, avg_domains_by_oil, avg_sleep_by_oil, yes_no_frequency_by_oil, comportamental_by_oil, avg_baseline_vs_intervention, sleep_baseline_vs_intervention, adhesion_by_responsible, feeling_evolution, oil_resistance_by_fase, routine_change_by_fase

def preload_data():
    for query in q.values():
        query_execute(query)
    for fn in [avg_domains_by_oil, avg_sleep_by_oil, yes_no_frequency_by_oil, comportamental_by_oil, avg_baseline_vs_intervention, sleep_baseline_vs_intervention, adhesion_by_responsible, feeling_evolution, oil_resistance_by_fase, routine_change_by_fase]:
        query_execute(fn())

PAGES = [
    st.Page("sections/general.py", title="Visão Geral"),
    st.Page("sections/children.py", title="Criança"),
    st.Page("sections/comparisons.py", title="Comparações"),
    st.Page("sections/registers.py", title="Registros"),
]

credentials = {
    "usernames": {
        username: dict(data)
        for username, data in st.secrets["credentials"]["usernames"].items()
    }
}

authenticator = stauth.Authenticate(
    credentials=credentials,
    cookie_name=st.secrets["cookie"]["name"],
    cookie_key=st.secrets["cookie"]["key"],
    cookie_expiry_days=st.secrets["cookie"]["expiry_days"]
)

MAX_LOGIN_ATTEMPTS = 5

def audit_log(usuario, acao):
    try:
        mydb = mysql.connector.connect(
            host=st.secrets["database"]["host"],
            port=int(st.secrets["database"]["port"]),
            user=st.secrets["database"]["user"],
            password=st.secrets["database"]["password"],
            database=st.secrets["database"]["database"]
        )
        cursor = mydb.cursor()
        cursor.execute(
            "INSERT INTO auditoria (usuario, acao) VALUES (%s, %s)",
            (usuario, acao)
        )
        mydb.commit()
        cursor.close()
        mydb.close()
    except Exception:
        pass

if st.session_state.get("logout") is True and not st.session_state.get("_logout_registered"):
    audit_log(st.session_state.get("_current_user"), "LOGOUT")
    st.session_state["_logout_registered"] = True

if not st.session_state.get("authentication_status"):
    st.navigation(PAGES, position="hidden")

    blocked = any(
        dict(data).get("failed_login_attempts", 0) >= MAX_LOGIN_ATTEMPTS
        for data in st.secrets["credentials"]["usernames"].values()
    )

    if blocked:
        st.error("Acesso temporariamente bloqueado. Entre em contato com o administrador.")
        st.stop()

    prev_status = st.session_state.get("authentication_status")
    authenticator.login(location="main")
    curr_status = st.session_state.get("authentication_status")

    if curr_status is True and prev_status is not True:
        audit_log(st.session_state.get("username"), "LOGIN")
    elif curr_status is False and prev_status is not False:
        audit_log(st.session_state.get("username", "desconhecido"), "LOGIN_FALHA")
        st.error("Usuário ou senha incorretos.")
    else:
        st.info("Por favor, faça login para acessar o sistema.")
    st.stop()

with st.sidebar:
    preload_data()
    st.write(f"Olá, {st.session_state['name']}")
    st.session_state["_current_user"] = st.session_state.get("username")
    if not st.session_state.get("logout"):
        st.session_state["_logout_registered"] = False
    authenticator.logout("Sair")

st.navigation(PAGES, position="sidebar").run()
