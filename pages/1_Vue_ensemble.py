import streamlit as st
import pandas as pd
import numpy as np
from utils import sidebar_filters, apply_filters
import app as mn
st.set_page_config(layout="wide")


df = mn.data1
f = sidebar_filters(df)
dff = apply_filters(df, f)

st.title("📊 Vue d’ensemble")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Période", f"{dff['year'].min()} → {dff['year'].max()}")
c2.metric("Observations", f"{len(dff):,}".replace(",", " "))
c3.metric("Régions", dff["region"].nunique())
c4.metric("Fédérations", dff["nom_fed"].nunique())

st.subheader("Aperçu des données")
st.dataframe(dff.head(50), use_container_width=True)

