import streamlit as st
import pandas as pd
import os
import plotly.express as px

# --- Page Config ---
st.set_page_config(page_title="SheEconomy Dashboard", layout="wide")

# --- Shared Data Directory ---
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)  # Ensure the folder exists

def get_path(filename):
    """Return the full path of a file inside the data directory."""
    return os.path.join(DATA_DIR, filename)

def load_data(filename):
    """Load CSV safely, return empty DataFrame if not found."""
    file_path = get_path(filename)
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        return pd.read_csv(file_path)
    else:
        return pd.DataFrame()

# --- Load Data ---
entrepreneurs = load_data("entrepreneurs.csv")
distribution = load_data("distribution_data.csv")
refill = load_data("refill_requests.csv")

# --- Dashboard Header ---
st.title("💼 SheEconomy Admin Dashboard")
st.markdown("Empowering women entrepreneurs through community-driven distribution 💖")

# --- Metrics ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Entrepreneurs", len(entrepreneurs))
col2.metric("Distributions", len(distribution))
col3.metric("Pads Distributed", int(distribution["Pads_Distributed"].sum()) if not distribution.empty else 0)
col4.metric("Refill Requests", len(refill))

st.markdown("---")

# --- Entrepreneurs Section ---
st.subheader("👩‍💼 Registered Entrepreneurs")
if not entrepreneurs.empty:
    st.dataframe(entrepreneurs, use_container_width=True)
else:
    st.info("No entrepreneur data available yet.")

# --- Distribution Section ---
st.subheader("📦 Distribution Records")
if not distribution.empty:
    st.dataframe(distribution, use_container_width=True)

    try:
        fig = px.bar(
            distribution,
            x="Date",
            y="Pads_Distributed",
            color="Area",
            title="Pads Distributed Over Time"
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.warning(f"Error displaying chart: {e}")
else:
    st.info("No distribution data available yet.")

# --- Refill Section ---
st.subheader("🔄 Refill Requests")
if not refill.empty:
    st.dataframe(refill, use_container_width=True)
else:
    st.info("No refill requests yet.")
