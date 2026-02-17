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

st.title("🚻 Analyse Hommes / Femmes")

sex = dff.groupby("annee")[["total_h", "total_f"]].sum().reset_index()
sex["total"] = sex["total_h"] + sex["total_f"]
sex["part_h"] = sex["total_h"] / sex["total"] * 100
sex["part_f"] = sex["total_f"] / sex["total"] * 100

c1, c2, c3 = st.columns(3)
c1.metric("Moyenne hommes (%)", f"{sex['part_h'].mean():.1f}")
c2.metric("Moyenne femmes (%)", f"{sex['part_f'].mean():.1f}")
c3.metric("Total période", f"{sex['total'].sum():,.0f}".replace(",", " "))

mode = st.radio("Affichage", ["Volumes", "Parts (%)"], horizontal=True)

if mode == "Volumes":
    fig = px.line(sex, x="annee", y=["total_h", "total_f"], markers=True,
                  title="Évolution des licences par sexe")
else:
    fig = px.line(sex, x="annee", y=["part_h", "part_f"], markers=True,
                  title="Parts (%) par sexe")

st.plotly_chart(fig, use_container_width=True)
st.dataframe(sex, use_container_width=True)
