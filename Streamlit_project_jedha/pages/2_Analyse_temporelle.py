import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    return pd.read_csv("data/licenses_by_year_region_fed.csv")

from utils import sidebar_filters, apply_filters

df = load_data()
f = sidebar_filters(df)
dff = apply_filters(df, f)

st.title("📈 Analyse temporelle")

metric = st.selectbox("Indicateur", ["total_license", "total_h", "total_f"])
ts = dff.groupby("annee")[metric].sum().reset_index()
ts["variation_%"] = ts[metric].pct_change() * 100

c1, c2 = st.columns(2)
with c1:
    st.dataframe(ts, use_container_width=True)

with c2:
    mode = st.radio("Affichage", ["Niveau", "Variation (%)"], horizontal=True)
    if mode == "Niveau":
        fig = px.line(ts, x="annee", y=metric, markers=True, title=f"Évolution — {metric}")
    else:
        fig = px.bar(ts, x="annee", y="variation_%", title=f"Variation annuelle (%) — {metric}")
    st.plotly_chart(fig, use_container_width=True)
