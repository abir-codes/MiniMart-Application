import streamlit as st
from setup import get_connection
import hashlib
import time

def hash_password(password):
    return  hashlib.sha256(password.encode()).hexdigest()


def signup(username,password):
    conn= get_connection()
    cursor = conn.cursor()
    
    check_query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(check_query, (username,))
    if cursor.fetchone():
        st.warning("Username already exists. Please choose another.")
    else:
        hashed_pw = hash_password(password)
        insert_query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cursor.execute(insert_query, (username, hashed_pw))
        conn.commit()
        st.success("Signed up successfully. Now log in to continue.")
    

def login(username,password):
    conn =  get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username =%s AND password =%s"
    hashed_pw = hash_password(password)

    cursor.execute(query,(username,hashed_pw))
    results = cursor.fetchone()
    if results:
        st.session_state.logged_in = True
        st.session_state.user_id = results[0]
        st.session_state.user_name = username
        st.success(f"Welcome {username} to Minimart")
        st.write("Session User ID:", st.session_state.get("user_id"))
        time.sleep(2)
        st.rerun()
    else:
         st.error("Login failed.")

    

def auth_ui():
    st.header("Login/Signup")
    username = st.text_input("Enter username")
    password = st.text_input("Enter password",type = "password")

    option = st.sidebar.radio("Signup/Login",["Signup","Login"])
    if option =="Signup":
        if st.button("Signup"):
            signup(username,password)
            

    if option == "Login":
        if st.button("Login"):
             login(username,password)
            

            
         