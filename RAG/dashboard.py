import streamlit as st
import json
import os
import pandas as pd

st.title("📊 AI Trust Dashboard")

if not os.path.exists("metrics.json"):
    st.info("No metrics yet")
    st.stop()

with open("metrics.json", "r") as f:
    data = json.load(f)

df = pd.DataFrame(data)

st.metric("Total Queries", len(df))
st.metric("Average Quality", round(df["score"].mean(), 2))

st.subheader("Hallucination Risk")
st.bar_chart(df["risk"].value_counts())

st.subheader("Intent Distribution")
st.bar_chart(df["intent"].value_counts())
