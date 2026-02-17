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

st.title("⚖️ Parité dans les fédérations")

min_total = st.slider("Seuil minimal de licences sur la période", 0, 200000, 10000, step=1000)

parite = dff.groupby("nom_fed").agg(total_license=("total_license","sum"),
                                   total_f=("total_f","sum"),
                                   total_h=("total_h","sum")).reset_index()
parite["part_femmes"] = parite["total_f"] / parite["total_license"] * 100
parite = parite[parite["total_license"] > min_total].sort_values("part_femmes", ascending=False)

c1, c2 = st.columns(2)
with c1:
    st.subheader("Top 10 — les plus féminisées")
    st.dataframe(parite.head(10)[["nom_fed","part_femmes","total_license"]], use_container_width=True)
with c2:
    st.subheader("Top 10 — les moins féminisées")
    st.dataframe(parite.tail(10)[["nom_fed","part_femmes","total_license"]].sort_values("part_femmes"),
                 use_container_width=True)

fig = px.histogram(parite, x="part_femmes", nbins=30, title="Distribution de la part des femmes (%)")
st.plotly_chart(fig, use_container_width=True)
