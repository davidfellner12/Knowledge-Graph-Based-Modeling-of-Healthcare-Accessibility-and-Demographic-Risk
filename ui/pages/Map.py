import streamlit as st
import pandas as pd
import pydeck as pdk
import requests

API = "http://127.0.0.1:5000"

st.title("🗺️ Healthcare Risk Map")

districts = pd.read_csv("data/processed/districts_enriched.csv")

# ---------------------------
# SIDEBAR INFO (WHAT IS RISK?)
# ---------------------------
with st.sidebar:
    st.header("ℹ️ What is this?")
    st.write("""
    The risk score combines:
    - Elderly population share
    - Hospital accessibility (distance)
    - Population density pressure
    - Graph-based learned vulnerability (GraphSAGE)
    """)

    st.markdown("### Interpretation")
    st.info("""
    🟢 Low risk: good access  
    🟡 Medium risk: moderate access  
    🔴 High risk: poor accessibility
    """)

# ---------------------------
# MAP
# ---------------------------
layer = pdk.Layer(
    "ScatterplotLayer",
    data=districts,
    get_position='[lon, lat]',
    get_radius=4000,
    get_fill_color='[255 - risk_score*120, risk_score*120, 100]',
    pickable=True,
)

view_state = pdk.ViewState(
    latitude=districts["lat"].mean(),
    longitude=districts["lon"].mean(),
    zoom=6
)

tooltip = {
    "html": """
    <b>District:</b> {district}<br/>
    <b>Risk:</b> {risk_score}<br/>
    <b>Population:</b> {population}<br/>
    <b>Elderly %:</b> {elderly_pct}
    """,
    "style": {"backgroundColor": "black", "color": "white"}
}

st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip=tooltip
))

# ---------------------------
# CLICK-STYLE EXPLORER
# ---------------------------
st.subheader("🔍 District Detail Explorer")

selected = st.selectbox("Choose district", districts["district"])

if st.button("Analyze"):
    res = requests.get(f"{API}/district/{selected}").json()

    st.metric("Risk Score", round(res["risk_score"], 3))
    st.metric("Nearest Hospital (km)", round(res["nearest_hospital_km"], 2))

    st.write("### Explanation (KG + Geo + ML)")
    st.json(res["explanation"])