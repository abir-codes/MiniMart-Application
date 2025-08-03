import streamlit as st
from auth import auth_ui
from etl_analytics import analytics
from stocks import stocks
from sales import sales
from expenses import expense
from alerts import warning
from setup import write_ca_cert

ca_path = write_ca_cert()
st.set_page_config(page_title="MiniMart App",layout ="wide")


if st.session_state.get("logged_in", False):

    st.sidebar.title("📊 MiniMart Dashboard")
    menu = st.sidebar.radio("Choose Section:", 
                            ["📦 Stock", "🛍️ Sales", "💸 Expense", "📈 Analytics", "⚠️ Alerts"])

    if menu == "📦 Stock":
        stocks()

    elif menu == "🛍️ Sales":
        sales()
    
    elif menu =="📈 Analytics":
        analytics()

    elif menu == "💸 Expense":
        expense()
    
    elif menu == "⚠️ Alerts":
        warning()

    
    if st.sidebar.button("🔓 Logout"):
        st.session_state.logged_in = False
        st.rerun()

else:
    auth_ui()