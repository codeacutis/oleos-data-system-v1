import view.config as config
import pandas as pd
import streamlit as st
import mysql.connector

@st.cache_resource
def connection():
    return mysql.connector.connect(
        host=st.secrets["database"]["host"],
        port=int(st.secrets["database"]["port"]),
        user=st.secrets["database"]["user"],
        password=st.secrets["database"]["password"],
        database=st.secrets["database"]["database"]
    )

def query_execute(query, params=None):
    mydb = connection()
    return pd.read_sql_query(query, mydb, params=params)