import streamlit as st
import pandas as pd
import plotly.express as px
import app as mn
from utils import sidebar_filters, apply_filters

df = mn.data1
f = sidebar_filters(df)
dff = apply_filters(df, f)

st.title("📈 Analyse temporelle")

metric = st.selectbox("Indicateur", ["total_lic", "total_h", "total_f"])
ts = dff.groupby("year")[metric].sum().reset_index()
ts["variation_%"] = ts[metric].pct_change() * 100

c1, c2 = st.columns(2)
with c1:
    st.dataframe(ts, use_container_width=True)

with c2:
    mode = st.radio("Affichage", ["Niveau", "Variation (%)"], horizontal=True)
    if mode == "Niveau":
        fig = px.line(ts, x="year", y=metric, markers=True, title=f"Évolution — {metric}")
    else:
        fig = px.bar(ts, x="year", y="variation_%", title=f"Variation annuelle (%) — {metric}")
    st.plotly_chart(fig, use_container_width=True)
