import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config
import streamlit as st
import streamlit_authenticator as stauth

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

if not st.session_state.get("authentication_status"):
    st.navigation(PAGES, position="hidden")
    authenticator.login(location="main")
    if st.session_state.get("authentication_status") is False:
        st.error("Usuário ou senha incorretos.")
    else:
        st.info("Por favor, faça login para acessar o sistema.")
    st.stop()

with st.sidebar:
    st.write(f"Olá, {st.session_state['name']}")
    authenticator.logout("Sair")

st.navigation(PAGES, position="sidebar").run()
