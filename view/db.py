import view.config as config
import pandas as pd
import streamlit as st
from load.db_connection import get_connection

@st.cache_resource
def connection():
    mydb = get_connection()
    return mydb

def query_execute(query, params=None):
    mydb = connection()
    return pd.read_sql_query(query, mydb, params=params)