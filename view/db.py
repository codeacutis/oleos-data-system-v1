import view.config as config
import pandas as pd
import streamlit as st
import os
from load.db_connection import get_connection

os.environ["DB_HOST"] = st.secrets["database"]["host"]
os.environ["DB_PORT"] = str(st.secrets["database"]["port"])
os.environ["DB_USER"] = st.secrets["database"]["user"]
os.environ["DB_PASSWORD"] = st.secrets["database"]["password"]
os.environ["DB_NAME"] = st.secrets["database"]["database"]

@st.cache_resource
def connection():
    return get_connection()

def query_execute(query, params=None):
    mydb = connection()
    return pd.read_sql_query(query, mydb, params=params)