import streamlit as st
import pandas as pd
import requests

API = "http://127.0.0.1:5000"

st.title("🧠 AI Explainability Layer (KG + GNN + Geo)")

districts = pd.read_csv("data/processed/districts_enriched.csv")

d = st.selectbox("Select district", districts["district"])

if st.button("Explain Risk Reasoning"):

    res = requests.get(f"{API}/district/{d}").json()

    st.subheader("🔎 Why this district is risky")

    st.write("### GraphSAGE learned factors")
    st.json(res["ml_factors"])

    st.write("### Knowledge Graph reasoning (rules)")
    st.json(res["kg_relations"])

    st.write("### Geo reasoning")
    st.json(res["geo"])