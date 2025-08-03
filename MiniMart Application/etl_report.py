
import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
import urllib.parse
from setup import write_ca_cert


def get_engine():
    
    ca_path = write_ca_cert()
    with open(ca_path, "w") as f:
        f.write(st.secrets["mysql"]["ca_cert"])

    host = st.secrets["mysql"]["host"]
    user = st.secrets["mysql"]["user"]
    password = urllib.parse.quote_plus(st.secrets["mysql"]["password"])
    port = st.secrets["mysql"]["port"]
    database = st.secrets["mysql"]["database"]

    connection_url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

    ssl_args = {
        "ssl": {
            "ca": ca_path
        }
    }

    return create_engine(connection_url, connect_args=ssl_args)



def filtered_stocks():
    engine = get_engine()
    stocks_data = pd.read_sql("SELECT * FROM stocks",con = engine)
    stocks_raw = pd.DataFrame(stocks_data)
    
    stocks_raw = stocks_raw[stocks_raw["product_name"].astype(str).str.strip().replace('',pd.NA).notna()]
    stocks_raw.fillna({"current_quantity":0,"minimum_quantity":0,"purchased_price":0,"selling price":0},inplace = True)
    stocks_raw.rename(columns={"current_quantity":"Added Stocks","minimum_quantity":"Minimum Stocks","last_updated":"Updated on","product_name":"Product","selling_price":"Selling Price","purchased_price":"Purchased Price"},inplace=True)
    stocks_raw.reset_index(drop=True,inplace=True)
    return stocks_raw

def filtered_expenses():
    engine = get_engine()
    expenses_data = pd.read_sql("SELECT * FROM expenses ",con = engine)
    expenses_raw = pd.DataFrame(expenses_data)
    
    expenses_raw = expenses_raw[expenses_raw["expense"].astype(str).str.strip().replace('',pd.NA).notna()]
    expenses_raw.fillna({"expense":0},inplace = True)
    expenses_raw.rename(columns={"expense":"Expense","price":"Price"},inplace=True)
    expenses_raw.reset_index(drop=True,inplace=True)
    return expenses_raw

def filtered_sales():
    engine = get_engine()
    sales_data = pd.read_sql("SELECT * FROM sales",con = engine)
    sales_raw = pd.DataFrame(sales_data)
    
    sales_raw = sales_raw[sales_raw["product_name"].astype(str).str.strip().replace('',pd.NA).notna()]
    sales_raw.fillna({"quantity":0,"total_price":0},inplace = True)
    sales_raw.rename(columns={"product_name":"Product","quantity":"No. of Stocks Sold","total_price":"Total Price"},inplace=True)
    sales_raw.reset_index(drop=True,inplace=True)
    return sales_raw

def combined():
    filter_sales = filtered_sales()
    filter_stocks = filtered_stocks()
    filtered_sales_df = filter_sales.groupby("Product").agg({"No. of Stocks Sold":"sum","Total Price":"sum"})
    combined_df = pd.merge(filter_stocks,filtered_sales_df,on="Product",how ="outer")
    combined_df["Remaining Stocks"] = combined_df["Added Stocks"] - combined_df["No. of Stocks Sold"]
    alerts_df = combined_df[combined_df["Minimum Stocks"]> combined_df["Remaining Stocks"]]
    return alerts_df,combined_df

