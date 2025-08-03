import streamlit as st
from setup import get_connection as connection
import datetime
from stocks import stocks
import time
from setup import write_ca_cert

def sales():
    ca_path = write_ca_cert()
    conn = connection()
    cursor = conn.cursor()
    user_id = st.session_state.user_id 
    query = "SELECT product_name from stocks WHERE user_id = %s"
    cursor.execute(query,(user_id,))
    stock_options = cursor.fetchall()
    if (stock_options):
        stocks = [row[0] for row in stock_options]
    else:
        st.error("No stocks to show")
    

    st.header("Sales")
    user_id = st.session_state.user_id 
    product_name = st.selectbox("Select item:",stocks)
    quantity = st.number_input("Enter the quantity of item")
    query ="SELECT selling_price FROM stocks WHERE product_name= %s"
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(query,(product_name,))
    sell_price = cursor.fetchone()[0]
    
    
    if st.button("Submit"):
        total_price = float(quantity)* float(sell_price)
        date_time = datetime.datetime.now()


        query = " INSERT INTO sales(user_id,product_name,quantity,total_price,date_time) VALUES(%s,%s,%s,%s,%s)"
        cursor.execute(query,(user_id,product_name,quantity,total_price,date_time))
        conn.commit()
        st.success("_Successfully added_")

        time.sleep(2)
        st.rerun()