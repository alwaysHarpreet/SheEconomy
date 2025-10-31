import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- Shared Data Folder ---
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def get_path(filename):
    """Get full path to a file inside the data directory."""
    return os.path.join(DATA_DIR, filename)

def save_data(filename, new_entry):
    """Append a new entry to a CSV file, create if not found."""
    file_path = get_path(filename)
    try:
        df = pd.read_csv(file_path)
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    except FileNotFoundError:
        df = pd.DataFrame([new_entry])
    df.to_csv(file_path, index=False)
    st.success("✅ Record saved successfully!")

# --- Page Setup ---
st.set_page_config(page_title="SheEconomy Portal", layout="wide")
st.title("👩‍💼 SheEconomy - Community Entrepreneur Portal")

# --- Sidebar Navigation ---
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Entrepreneur Registration", "Distribution Form", "Refill Request"])

# --- 1️⃣ Entrepreneur Registration ---
if section == "Entrepreneur Registration":
    st.header("🌐 Register a New Entrepreneur")
    with st.form("entrepreneur_form", clear_on_submit=True):
        name = st.text_input("Full Name")
        area = st.text_input("Area / Community")
        contact = st.text_input("Contact Number")
        experience = st.selectbox("Experience Level", ["Beginner", "Intermediate", "Expert"])
        submit = st.form_submit_button("Register Entrepreneur")

    if submit:
        if not name or not area:
            st.error("⚠️ Please fill out all required fields.")
        else:
            data = {
                "Name": name,
                "Area": area,
                "Contact": contact,
                "Experience": experience,
                "Registration_Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            save_data("entrepreneurs.csv", data)

# --- 2️⃣ Distribution Form ---
elif section == "Distribution Form":
    st.header("📦 Record Pad Distribution")
    with st.form("distribution_form", clear_on_submit=True):
        entrepreneur = st.text_input("Entrepreneur Name")
        area = st.text_input("Area / Community")
        pads_distributed = st.number_input("Number of Pads Distributed", min_value=1)
        date = st.date_input("Distribution Date", value=datetime.now())
        submit = st.form_submit_button("Submit Distribution")

    if submit:
        if not entrepreneur or not area:
            st.error("⚠️ Please fill out all required fields.")
        else:
            data = {
                "Entrepreneur": entrepreneur,
                "Area": area,
                "Pads_Distributed": pads_distributed,
                "Date": date
            }
            save_data("distribution_data.csv", data)

# --- 3️⃣ Refill Request ---
elif section == "Refill Request":
    st.header("🔄 Submit a Refill Request")
    with st.form("refill_form", clear_on_submit=True):
        entrepreneur = st.text_input("Entrepreneur Name")
        area = st.text_input("Area / Community")
        pads_needed = st.number_input("Pads Needed", min_value=10, step=10)
        urgency = st.selectbox("Urgency Level", ["Low", "Medium", "High"])
        submit = st.form_submit_button("Send Request")

    if submit:
        if not entrepreneur or not area:
            st.error("⚠️ Please fill out all required fields.")
        else:
            data = {
                "Entrepreneur": entrepreneur,
                "Area": area,
                "Pads_Requested": pads_needed,
                "Urgency": urgency,
                "Request_Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            save_data("refill_requests.csv", data)
