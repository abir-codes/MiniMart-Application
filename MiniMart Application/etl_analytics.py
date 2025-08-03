import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from etl_report import combined,filtered_sales,filtered_stocks
import matplotlib.pyplot as plt
from setup import write_ca_cert


def analytics():
  

    ca_path = write_ca_cert()
    user_id = st.session_state.user_id
    df_sales = filtered_sales()
    df_stocks = filtered_stocks
    df_sales["Date"] = df_sales["date_time"].dt.date
    df_sales["Month"] = df_sales["date_time"].dt.month_name()
    df_sales["Year"] = df_sales["date_time"].dt.year
    df_sales["Weekday"] = df_sales["date_time"].dt.day_name()

    df = pd.merge(df_sales,df_stocks()[["Product","Purchased Price","Selling Price"]],how= "left",on="Product")
    df["Estimated Profit (₹)"] = df["Total Price"] - df["No. of Stocks Sold"]*df["Purchased Price"]
    df = df[df["user_id"] == user_id]
    df_2 = df
    def product_wise_report(df_,condition):
        df_ = df_[condition]
        df_ = df_.groupby("Product").agg({"No. of Stocks Sold":"sum","Total Price":"sum","Estimated Profit (₹)":"sum"}).reset_index()
        return df_
    
    if st.button("See Today's Analytics"):
       condition_1 = df["Date"] == datetime.today().date()
       report = product_wise_report(df, condition_1)

       if report.empty:
        st.warning("No sales data available for today.")
       elif "Product" not in report.columns:
        st.error("'Product' column missing from report.")
        st.write(report)
       else:
        
        df = df.groupby("Product",as_index = False)["No. of Stocks Sold"].sum()
        sales = df["No. of Stocks Sold"]
        labels = df["Product"]
        st.header("No. of Stocks Sold")
        fig, ax = plt.subplots()
        ax.pie(sales, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig)

        st.header("Product-Wise Estimated Profit (₹)")
        st.bar_chart(report.set_index("Product")["Estimated Profit (₹)"])

    if st.button("See Monthly Analytics"):
           today = pd.to_datetime('today')
           current_month = today.month
           condition_2 = df["Month"] == current_month
           report = product_wise_report(df, condition_2)

           if report.empty:
               st.warning("No sales data available for this month.")
           elif "Product" not in report.columns:
               st.error("'Product' column missing from report.")
               st.write(report)
           else:
        
              df = df.groupby("Product",as_index = False)["No. of Stocks Sold"].sum()
              sales = df["No. of Stocks Sold"]
              labels = df["Product"]
              st.header("No. of Stocks Sold")
              fig, ax = plt.subplots()
              ax.pie(sales, labels=labels, autopct='%1.1f%%', startangle=90)
              ax.axis('equal')
              st.pyplot(fig)

              st.header("Product-Wise Estimated Profit (₹)")
              st.bar_chart(report.set_index("Product")["Estimated Profit (₹)"])

    if st.button("See Yearly Analytics"):
           today = pd.to_datetime('today')
           current_year = today.year
           condition_3= df["Year"] == current_year
           report = product_wise_report(df, condition_3)

           if report.empty:
               st.warning("No sales data available for this year.")
           elif "Product" not in report.columns:
               st.error("'Product' column missing from report.")
               st.write(report)
           else:
        
              df = df.groupby("Product",as_index = False)["No. of Stocks Sold"].sum()
              sales = df["No. of Stocks Sold"]
              labels = df["Product"]
              st.header("No. of Stocks Sold")
              fig, ax = plt.subplots()
              ax.pie(sales, labels=labels, autopct='%1.1f%%', startangle=90)
              ax.axis('equal')
              st.pyplot(fig)

              st.header("Product-Wise Estimated Profit (₹)")
              st.bar_chart(report.set_index("Product")["Estimated Profit (₹)"])    

    def time_frame_report(df_,time_frame,label):
        st.header(label)
        df_ = df_.groupby([time_frame,"Product"]).agg({"No. of Stocks Sold":"sum","Total Price":"sum","Estimated Profit (₹)":"sum"}).reset_index()
        return df_

    if not df.empty:
        month = time_frame_report(df_2,"Month","Month Wise Sales Comparison")
        st.dataframe(month)
        year = time_frame_report(df_2,"Year","Year Wise Sales Comparison")
        st.dataframe(year)
        day = time_frame_report(df_2,"Weekday","Weekday Wise Sales Comparison")
        st.dataframe(day)


    else:
        st.warning("No data found")

            

           


        
