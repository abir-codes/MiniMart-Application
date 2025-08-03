import pandas as pd
import streamlit as st
from etl_report import combined
from setup import write_ca_cert

def warning():
  ca_path = write_ca_cert()
  if st.button("Click here to see low stock alerts"):
    alert_df,combined_df = combined()
    if not alert_df.empty:
        
        user_id = st.session_state.user_id
        filter_alerts_df = alert_df[alert_df["user_id"] == user_id]
        filter_alerts_df = filter_alerts_df[["Product","Minimum Stocks","Remaining Stocks"]]
        if not filter_alerts_df.empty:
          st.warning("See below the lock stocks products:")
          st.dataframe(filter_alerts_df)
        else:
          st.error("No low stock products")
    else:
          st.error("No results found")