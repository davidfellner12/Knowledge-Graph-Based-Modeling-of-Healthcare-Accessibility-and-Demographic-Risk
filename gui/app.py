import streamlit as st
import pandas as pd
import pydeck as pdk
import requests

st.set_page_config(page_title="Healthcare KG System", layout="wide")

API = "http://127.0.0.1:5000"

st.title("🏥 Healthcare Accessibility & Risk Intelligence System")

districts = pd.read_csv("data/processed/districts_enriched.csv")

# ---------------------------
# MAP
# ---------------------------
st.header("🗺️ Risk Map (GraphSAGE)")

layer = pdk.Layer(
    "ScatterplotLayer",
    data=districts,
    get_position='[lon, lat]',
    get_radius=4000,
    get_fill_color='[255 - risk_score*120, risk_score*100, 120]',
    pickable=True,
)

view_state = pdk.ViewState(
    latitude=districts["lat"].mean(),
    longitude=districts["lon"].mean(),
    zoom=6,
)

st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))

# ---------------------------
# TOP RISK FROM API
# ---------------------------
st.header("🔥 Top Risk Districts (API)")

if st.button("Load Top Risk Areas"):
    res = requests.get(f"{API}/risk/top").json()
    st.dataframe(pd.DataFrame(res))

# ---------------------------
# SINGLE QUERY
# ---------------------------
st.header("🔍 District Explorer")

name = st.text_input("District name")

if st.button("Search"):
    res = requests.get(f"{API}/district/{name}").json()
    st.json(res)