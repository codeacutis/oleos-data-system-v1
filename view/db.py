import mysql.connector
import pandas as pd
import streamlit as st

def get_connection():
    return mysql.connector.connect(
        host=st.secrets["database"]["host"],
        port=int(st.secrets["database"]["port"]),
        user=st.secrets["database"]["user"],
        password=st.secrets["database"]["password"],
        database=st.secrets["database"]["database"]
    )

@st.cache_data(ttl=300)
def query_execute(query, params=None):
    mydb = get_connection()
    try:
        return pd.read_sql_query(query, mydb, params=params)
    finally:
        mydb.close()