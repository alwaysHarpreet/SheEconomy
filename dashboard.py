import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import plotly.express as px

st.set_page_config(page_title="SheEconomy Dashboard", layout="wide")

# ✅ Authenticate with Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(st.secrets["google_service_account"], scopes=scope)
client = gspread.authorize(creds)

SHEET_ID = "1gNDTITlIJ26Ja-zu7NYjsOBeMGuknjgiMb13l-goATQ"
sheet = client.open_by_key(SHEET_ID)

# Function to load each sheet
def get_data(sheet_name):
    try:
        ws = sheet.worksheet(sheet_name)
        data = ws.get_all_records()
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Error loading {sheet_name}: {e}")
        return pd.DataFrame()

# Load data
entrepreneurs = get_data("entrepreneurs")
distribution = get_data("distribution_data")
refill = get_data("refill_requests")

# --- Dashboard UI ---
st.title("💼 SheEconomy Admin Dashboard")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Entrepreneurs", len(entrepreneurs))
col2.metric("Distributions", len(distribution))
col3.metric("Pads Distributed", distribution["Pads_Distributed"].astype(int).sum() if not distribution.empty else 0)
col4.metric("Refill Requests", len(refill))

st.markdown("---")

# Entrepreneurs Data
st.subheader("👩‍💼 Registered Entrepreneurs")
st.dataframe(entrepreneurs if not entrepreneurs.empty else pd.DataFrame())

# Distribution Data
st.subheader("📦 Distribution Records")
if not distribution.empty:
    fig = px.bar(
        distribution,
        x="Date",
        y="Pads_Distributed",
        color="Area",
        title="Pads Distributed Over Time",
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No distribution data yet.")

# Refill Requests
st.subheader("🔄 Refill Requests")
st.dataframe(refill if not refill.empty else pd.DataFrame())
