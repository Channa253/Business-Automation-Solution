import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Iron Pulse Admin", layout="wide", page_icon="🛡️")

# --- CUSTOM CSS & ANIMATIONS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@400;600&display=swap');

    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #2D0B0B 0%, #4A0E0E 100%);
        color: #FFFFFF;
    }

    /* Professional Font Styling */
    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: #FFD700 !important; /* Gold */
    }
    
    p, span, label {
        font-family: 'Inter', sans-serif !important;
    }

    /* Glassmorphism Card Effect */
    .stDataFrame, .stForm, div[data-testid="stMetricValue"] {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px !important;
        padding: 20px;
        transition: transform 0.3s ease;
    }

    /* Hover Animation */
    div[data-testid="stMetricValue"]:hover {
        transform: translateY(-5px);
        border-color: #FFD700;
    }

    /* Button Styling */
    .stButton>button {
        background: linear-gradient(90deg, #FFD700 0%, #BF953F 100%) !important;
        color: #2D0B0B !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 10px 25px !important;
        transition: all 0.3s ease !important;
    }

    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0px 0px 15px rgba(255, 215, 0, 0.4);
    }

    /* Success Message Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .stAlert {
        animation: fadeIn 0.5s ease-out;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE LOGIC ---
DB_FILE = "iron_lady_data.csv"
if not os.path.exists(DB_FILE):
    df = pd.DataFrame(columns=["ID", "Date Joined", "Name", "Buddy Group", "B-HAG Goal", "Status"])
    # Adding some dummy data for the video demo
    dummy_data = [
        [1, "2026-01-15", "Anjali Sharma", "Alpha", "Launch Tech Startup", "Milestone 2"],
        [2, "2026-01-20", "Priya Nair", "Beta", "Board Member Seat", "Started"]
    ]
    df = pd.DataFrame(dummy_data, columns=df.columns)
    df.to_csv(DB_FILE, index=False)

def load_data(): return pd.read_csv(DB_FILE)
def save_data(data): data.to_csv(DB_FILE, index=False)

# --- APP LAYOUT ---
st.title("🛡️ Iron Pulse: Internal Ops")
st.write("Streamlining Leadership Excellence through Automated Coordination.")
st.markdown("---")

df = load_data()

# --- TOP METRICS (Efficiency Demo) ---
col1, col2, col3 = st.columns(3)
col1.metric("Active Leaders", len(df))
col2.metric("Efficiency Gain", "85%", "12h saved/wk")
col3.metric("Goal Completion", "92%")

st.sidebar.image("https://via.placeholder.com/150x150.png?text=IRON+LADY", width=100) # Replace with real logo URL if you have it
menu = ["📈 Dashboard", "➕ Add Participant", "🔄 Update Progress", "🗑️ Archive Record"]
choice = st.sidebar.radio("Navigation", menu)

# --- CREATE ---
if choice == "➕ Add Participant":
    st.subheader("Register New Leader")
    with st.form("add_form", clear_on_submit=True):
        name = st.text_input("Full Name")
        group = st.selectbox("Buddy Group Assignment", ["Alpha", "Beta", "Gamma", "Delta", "Epsilon"])
        bhag = st.text_area("B-HAG (Big Hairy Audacious Goal)")
        if st.form_submit_button("Confirm Onboarding"):
            new_row = [len(df)+1, datetime.now().strftime("%Y-%m-%d"), name, group, bhag, "Started"]
            df.loc[len(df)] = new_row
            save_data(df)
            st.success(f"Successfully onboarded {name}!")

# --- READ ---
elif choice == "📈 Dashboard":
    st.subheader("Cohort Overview")
    st.dataframe(df, use_container_width=True)
    st.info("💡 Note: This live view replaces the manual weekly CSV exports.")

# --- UPDATE ---
elif choice == "🔄 Update Progress":
    st.subheader("Modify Milestone Status")
    name_list = df["Name"].tolist()
    selected_user = st.selectbox("Select Participant", name_list)
    new_status = st.select_slider("New Status", options=["Started", "Milestone 1", "Milestone 2", "B-HAG Achieved"])
    
    if st.button("Update Progress"):
        df.loc[df["Name"] == selected_user, "Status"] = new_status
        save_data(df)
        st.balloons() # Visual celebration animation
        st.success(f"Status updated for {selected_user}!")

# --- DELETE ---
elif choice == "🗑️ Archive Record":
    st.subheader("Remove/Archive Participant")
    delete_user = st.selectbox("Select Record to Archive", df["Name"].tolist())
    if st.button("Archive Permanently"):
        df = df[df["Name"] != delete_user]
        save_data(df)
        st.warning(f"Record for {delete_user} has been archived.")