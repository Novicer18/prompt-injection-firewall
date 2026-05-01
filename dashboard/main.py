import streamlit as st
import pandas as pd
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
import plotly.express as px

load_dotenv()

# Page Config for that "Pro" look
st.set_page_config(page_title="AI Firewall Dashboard", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS to mimic the Dark "SOC" look
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Database Connection
engine = create_engine(os.getenv("DATABASE_URL"))

def load_data():
    query = "SELECT * FROM security_logs ORDER BY timestamp DESC"
    return pd.read_sql(query, engine)

st.title("🛡️ AI Prompt Firewall: Executive Security Overview")

try:
    df = load_data()

    # --- TOP ROW: KPI METRICS ---
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Requests", len(df))
    with col2:
        blocks = len(df[df['is_safe'] == False])
        st.metric("Threats Blocked", blocks, delta=f"{blocks} total", delta_color="inverse")
    with col3:
        avg_score = df['risk_score'].mean()
        st.metric("Avg Risk Score", f"{round(avg_score, 2)}")
    with col4:
        st.metric("System Status", "PROTECTED", delta="Active")

    # --- MIDDLE ROW: CHARTS ---
    st.divider()
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.subheader("Threat Activity Timeline")
        # Ensure timestamp is datetime for plotting
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        timeline = df.resample('h', on='timestamp').count()['id'].reset_index()
        fig_line = px.line(timeline, x='timestamp', y='id', title="Blocked Prompts per Hour")
        st.plotly_chart(fig_line, use_container_width=True)

    with c2:
        st.subheader("Detection Engine Breakdown")
        fig_pie = px.pie(df, names='detection_layer', title="Who caught the threat?")
        st.plotly_chart(fig_pie, use_container_width=True)

    # --- BOTTOM ROW: RAW LOGS ---
    st.subheader("Recent Security Events")
    st.dataframe(df[['timestamp', 'prompt_text', 'detection_layer', 'decision', 'risk_score']], use_container_width=True)

except Exception as e:
    st.error(f"Waiting for data... Ensure the Firewall has run at least once. Error: {e}")