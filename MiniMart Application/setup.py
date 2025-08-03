import mysql.connector
from sqlalchemy import create_engine
import streamlit as st
import os

def get_connection():
    ca_path = write_ca_cert()
    connection = mysql.connector.connect(
    
        host = st.secrets["mysql"]["host"],
        user = st.secrets["mysql"]["user"],
        password = st.secrets["mysql"]["password"],
        database = st.secrets["mysql"]["database"],
        port = st.secrets["mysql"]["port"],
        ssl_ca = ca_path
    )
    
    return connection



  

def write_ca_cert():
    ca_path = ".streamlit/aiven-ca.pem"
    
    if "ca_cert_written" not in st.session_state:
        os.makedirs(".streamlit", exist_ok=True)
        with open(ca_path, "w") as f:
            f.write(st.secrets["mysql"]["ca_cert"])
        st.session_state["ca_cert_written"] = True
    
    return ca_path