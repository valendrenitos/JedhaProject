import streamlit as st
import pandas as pd
import plotly.express as px
import app as mn
from utils import sidebar_filters, apply_filters

df = mn.data1
f = sidebar_filters(df)
dff = apply_filters(df, f)

st.title("⚖️ Parité dans les fédérations")

min_total = st.slider("Seuil minimal de licences sur la période", 0, 200000, 10000, step=1000)

parite = dff.groupby("nom_fed", as_index=False).agg(total_license=("total_lic","sum"),
                                   total_f=("total_f","sum"),
                                   total_h=("total_h","sum"))
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
fig.update_layout(bargap=0.2)    
st.plotly_chart(fig, use_container_width=True)
