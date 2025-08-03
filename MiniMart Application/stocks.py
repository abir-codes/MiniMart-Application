import streamlit as st
from setup import get_connection as connection
from auth import auth_ui
import datetime
import time
import pandas as pd
from etl_report import filtered_stocks
from setup import write_ca_cert


def stocks():
    ca_path = write_ca_cert()
    st.header("Stocks")

    if st.button("Show all Stocks"):
       df = filtered_stocks() 
       if not df.empty:
            user_id = st.session_state.user_id
            df_finnal = df[df["user_id"]== user_id]
            df_finnal.reset_index(drop = True, inplace = True)
            df_finnal = df_finnal.drop(["user_id","stock_id"],axis = 1)
            st.dataframe(df_finnal)
            
       else:
           st.error("No stocks to display")
            
    st.subheader("Add Stocks")       
    
    with st.form("Add Form"):
            
            product_name = st.text_input("Enter item name :")
            selling_price = st.number_input("Enter selling price of each item")
            purchased_price = st.number_input("Enter purhasing price of each item")
            current_quantity = st.number_input("Enter current quantity")
            min_quantity = st.number_input("Enter minimum quantity")
            last_updated = datetime.date.today()
            if st.form_submit_button("Final Add"):
                user_id = st.session_state.user_id

                conn = connection()
                cursor = conn.cursor()
                query = " INSERT INTO stocks(user_id,product_name,selling_price,purchased_price,current_quantity,minimum_quantity,last_updated) VALUES(%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(query,(user_id,product_name,selling_price,purchased_price,current_quantity,min_quantity,last_updated))
                conn.commit()
                st.success("Added Successfully")
                time.sleep(2)
                st.rerun()
       
    user_id = st.session_state.user_id
    conn = connection()
    cursor = conn.cursor()
   
    df = filtered_stocks()
    df = df[df["user_id"]== user_id]
    products =  df["Product"]

    st.subheader("Delete Stock")
    
    if not products.empty:
         with st.form("Delete Form"):
              product_to_delete = st.selectbox("Select product to delete",products)
              delete_button = st.form_submit_button("Final Delete")
              if delete_button:
                   query = "DELETE FROM stocks WHERE user_id=%s AND product_name=%s"
                   cursor.execute(query,(st.session_state.user_id,product_to_delete))
                   conn.commit()
                   st.success(f"Deleted: {product_to_delete}")
              else:
                   st.warning("No products available to display")
    
     
    st.subheader("Edit Stock")

    if not products.empty:
     with st.form("Edit Form"):
        product_to_edit = st.selectbox("Select product to edit", products)
        results = df[["Selling Price","Purchased Price","Minimum Stocks","Added Stocks"]][df["Product"] == product_to_edit]
        
        if not results.empty:
            st.success("Successfully fetched")

            previous_selling_price = float(results["Selling Price"])
            previous_purchasing_price = float(results["Purchased Price"])
            previous_added_quant = float(results["Added Stocks"])
            previous_min_quant = float(results["Minimum Stocks"])

            new_selling_price = st.number_input("Edit selling price", value=previous_selling_price, step=1.0)
            new_purchasing_price = st.number_input("Edit purchased price", value=previous_purchasing_price, step=1.0)
            new_current_quantity = st.number_input("Edit current quantity", value=previous_added_quant, step=1.0)
            new_min_quant = st.number_input("Edit minimum quantity", value=previous_min_quant, step=1.0)

            edit_button = st.form_submit_button("Final Edit")

            if edit_button:
                update_query = """
                UPDATE stocks 
                SET selling_price = %s, purchased_price = %s, current_quantity = %s, minimum_quantity = %s 
                WHERE user_id = %s AND product_name = %s
                """
                cursor.execute(update_query, (
                    new_selling_price,
                    new_purchasing_price,
                    new_current_quantity,
                    new_min_quant,
                    st.session_state.user_id,
                    product_to_edit
                ))
                conn.commit()
                st.success(f"Edited: {product_to_edit}")
            else:
              st.warning("No stock data found for the selected product.")
        else:
         st.warning("No products available to display")
