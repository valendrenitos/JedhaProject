import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("data/licenses_by_year_region_fed.csv")

from utils import sidebar_filters, apply_filters

df = load_data()
f = sidebar_filters(df)
dff = apply_filters(df, f)

st.title("📊 Vue d’ensemble")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Période", f"{dff['annee'].min()} → {dff['annee'].max()}")
c2.metric("Observations", f"{len(dff):,}".replace(",", " "))
c3.metric("Régions", dff["region"].nunique())
c4.metric("Fédérations", dff["nom_fed"].nunique())

st.subheader("Aperçu des données")
st.dataframe(dff.head(50), use_container_width=True)

