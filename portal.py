import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# Authenticate using Streamlit secrets
creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"])
client = gspread.authorize(creds)

# Open the Google Sheet
SHEET_ID = "1gNDTITlIJ26Ja-zu7NYjsOBeMGuknjgiMb13l-goATQ"
sheet = client.open_by_key(SHEET_ID)

def append_row(worksheet_name, data_list):
    ws = sheet.worksheet(worksheet_name)
    ws.append_row(data_list, value_input_option="USER_ENTERED")

# --- Streamlit UI (same as before) ---
st.set_page_config(page_title="SheEconomy Portal", layout="wide")
st.title("👩‍💼 SheEconomy - Community Entrepreneur Portal")
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Entrepreneur Registration", "Distribution Form", "Refill Request"])

if section == "Entrepreneur Registration":
    st.header("🌐 Register a New Entrepreneur")
    with st.form("entrepreneur_form", clear_on_submit=True):
        name = st.text_input("Full Name")
        area = st.text_input("Area / Community")
        contact = st.text_input("Contact Number")
        experience = st.selectbox("Experience Level", ["Beginner", "Intermediate", "Expert"])
        submit = st.form_submit_button("Register Entrepreneur")
    if submit:
        append_row("entrepreneurs", [name, area, contact, experience, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
        st.success("✅ Entrepreneur registered successfully!")

elif section == "Distribution Form":
    st.header("📦 Record Pad Distribution")
    with st.form("distribution_form", clear_on_submit=True):
        entrepreneur = st.text_input("Entrepreneur Name")
        area = st.text_input("Area / Community")
        pads_distributed = st.number_input("Number of Pads Distributed", min_value=1)
        date = st.date_input("Distribution Date", value=datetime.now())
        submit = st.form_submit_button("Submit Distribution")
    if submit:
        append_row("distribution_data", [entrepreneur, area, pads_distributed, str(date)])
        st.success("✅ Distribution recorded successfully!")

elif section == "Refill Request":
    st.header("🔄 Submit a Refill Request")
    with st.form("refill_form", clear_on_submit=True):
        entrepreneur = st.text_input("Entrepreneur Name")
        area = st.text_input("Area / Community")
        pads_needed = st.number_input("Pads Needed", min_value=10, step=10)
        urgency = st.selectbox("Urgency Level", ["Low", "Medium", "High"])
        submit = st.form_submit_button("Send Request")
    if submit:
        append_row("refill_requests", [entrepreneur, area, pads_needed, urgency, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
        st.success("✅ Refill request sent successfully!")
