import streamlit as st
from setup import get_connection as connection
import datetime
import time 
import pandas as pd
from etl_report import filtered_expenses
from setup import write_ca_cert

def expense():
    ca_path = write_ca_cert()
    st.header("Expenses")

    if st.button("Show Expenses"):
          df = filtered_expenses()
          if not df.empty:
            user_id = st.session_state.user_id
            df_final = df[df["user_id"] == user_id]
            df_final.reset_index(drop = True, inplace = True)
            df_final = df_final.drop(["user_id","expense_id"],axis = 1)
            st.dataframe(df_final)
            
          else:
           st.error("No stocks to display")
       

    st.subheader("Add Expenses")
    with st.form("Add Form"):
       expense = st.text_input("Enter expense :")
       price = st.number_input("Enter the price of item")
       date_time = datetime.datetime.now()
   
       if st.form_submit_button("Final Add"):
       
        user_id = st.session_state.user_id
        conn = connection()
        cursor = conn.cursor()
        query = "INSERT INTO expenses(user_id,expense,price,date_time) VALUES(%s,%s,%s,%s)"
        cursor.execute(query,(user_id,expense,price,date_time))
        conn.commit()
        st.success("Added Successfully")
        time.sleep(2)
        
        st.rerun()
    
    
    user_id = st.session_state.user_id
    conn = connection()
    df = filtered_expenses()
    df = df[df["user_id"] == user_id]
    results1 = df["Expense"]
  
    
    st.subheader(" Delete Expenses")
    if not df.empty:
      with st.form("Delete Form"):
           expense = st.selectbox("Select expense to delete:",results1)
    
           if st.form_submit_button("Final Delete"):
       
              user_id = st.session_state.user_id
              cursor = conn.cursor()
              query = "DELETE FROM expenses where expense = %s AND user_id = %s"
              cursor.execute(query,(expense,user_id))
              conn.commit()
              st.success("Deleted Successfully")
              time.sleep(2)
        
              st.rerun()
    else:
        st.warning("No expenses to delete")

    st.subheader("Edit Expenses")
    if not df.empty:
      with st.form("Edit Form"):
       
           expense = st.selectbox("Select expense to edit:",results1)
           previous_price = float(df["Price"][df["Expense"]== expense])
           new_price = st.number_input("Enter new price:",value = previous_price,step =1.00)
        
           if st.form_submit_button("Final Edit"):
           
             user_id = st.session_state.user_id
             conn = connection()
             cursor = conn.cursor()
             query = "UPDATE expenses SET price = %s WHERE expense = %s AND user_id = %s "
             cursor.execute(query,(new_price,expense,user_id))
             conn.commit
             st.success("Successfully Edited")
             time.sleep(2)
             st.rerun()
        
    else:
           st.warning("No expenses to edit")
        