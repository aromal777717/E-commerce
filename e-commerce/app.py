import streamlit as st
import pandas as pd
import plotly.express as px

# --- EXECUTIVE THEME CONFIG ---
st.set_page_config(page_title="Cloud Cost Intelligence", layout="wide")

# This CSS makes the background dark and the metric cards pop
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="stMetricValue"] { color: #00d4ff; font-size: 32px; }
    div[data-testid="metric-container"] {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 20px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🌐 Cloud Cost Intelligence Dashboard")
st.markdown("---")

# --- SIDEBAR: DATA INGESTION ---
st.sidebar.header("Admin Controls")
uploaded_file = st.sidebar.file_uploader("Upload Billing CSV", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    # --- EXECUTIVE KPI RIBBON ---
    k1, k2, k3 = st.columns(3)
    k1.metric("Total Infrastructure Spend", f"${df['Cost'].sum():,.2f}")
    k2.metric("Primary Cost Center", df.groupby('Service Type')['Cost'].sum().idxmax())
    k3.metric("Data Records", f"{len(df)} Items")

    st.markdown("### Financial Analytics Overview")
    
    # --- CHART GRID ---
    col1, col2 = st.columns(2)

    with col1:
        # Pie Chart with Dark Template
        fig_pie = px.pie(df, values='Cost', names='Service Type', hole=0.5,
                         template="plotly_dark", color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        # Bar Chart with Dark Template
        fig_bar = px.bar(df, x='Date', y='Cost', title="Daily Spend Trend",
                         template="plotly_dark", color='Service Type')
        st.plotly_chart(fig_bar, use_container_width=True)

    # --- GRANULAR DATA TABLE ---
    st.subheader("Filterable Billing Records")
    st.dataframe(df, use_container_width=True)
else:
    st.info("Awaiting CSV upload for analysis...")