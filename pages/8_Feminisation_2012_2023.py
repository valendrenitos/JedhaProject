import streamlit as st
import pandas as pd
import plotly.express as px
import app as mn
from utils import sidebar_filters, apply_filters

df =mn.data1
f = sidebar_filters(df)
dff = apply_filters(df, f)

st.title("📌 Féminisation 2012 → 2023")

evol = dff.groupby(["nom_fed","year"], as_index=False).agg(total_license=("total_lic","sum"),
                                           total_f=("total_f","sum"),
                                           total_h=("total_h","sum"))
evol["part_femmes"] = evol["total_f"] / evol["total_license"] * 100

p2012 = evol[evol["year"] == 2012][["nom_fed","part_femmes"]].rename(columns={"part_femmes":"part_femmes_2012"})
p2023 = evol[evol["year"] == 2023][["nom_fed","part_femmes"]].rename(columns={"part_femmes":"part_femmes_2023"})

evo = p2012.merge(p2023, on="nom_fed", how="inner")
evo["variation_absolue"] = evo["part_femmes_2023"] - evo["part_femmes_2012"]
evo["variation_relative"] = (evo["part_femmes_2023"] / evo["part_femmes_2012"] - 1) * 100

tot = dff.groupby("nom_fed")["total_lic"].sum().reset_index().rename(columns={"total_lic":"total_licences_periode"})
evo = evo.merge(tot, on="nom_fed", how="left").sort_values("variation_absolue", ascending=False)

top_n = st.slider("Top N", 5, 50, 20)
st.subheader(f"Top {top_n} fédérations — plus forte hausse de la part des femmes")
st.dataframe(evo.head(top_n), use_container_width=True)

# Bonus : choisir une fédération et tracer la série temporelle de part_femmes
st.subheader("Évolution annuelle (sélection)")
fed = st.selectbox("Choisir une fédération", sorted(evol["nom_fed"].unique()))
curve = evol[evol["nom_fed"] == fed].sort_values("year")
fig = px.line(curve, x="year", y="part_femmes", markers=True, title=f"Part des femmes — {fed}")
st.plotly_chart(fig, use_container_width=True)
