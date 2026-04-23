import streamlit as st
import pandas as pd

districts = pd.read_csv("data/processed/districts_enriched.csv")

st.title("🏥 Healthcare Accessibility Knowledge Graph")

district = st.selectbox("Select District", districts["district"])

row = districts[districts["district"] == district].iloc[0]

st.subheader("📊 District Overview")

st.write("Population:", int(row["population"]))
st.write("Elderly %:", float(row["elderly_pct"]))
st.write("Nearest Hospital (km):", float(row["nearest_hospital_km"]))
st.write("Risk Score:", float(row["risk_score"]))

if row["risk_score"] > 0.6:
    st.error("⚠ High Risk Area")
elif row["risk_score"] > 0.3:
    st.warning("Moderate Risk")
else:
    st.success("Low Risk")


st.subheader("🚨 High Risk Districts")

st.dataframe(districts[districts["risk_score"] > 0.6])