import streamlit as st
import pandas as pd
import plotly.express as px
import app as mn
from utils import sidebar_filters, apply_filters


df = mn.data1
f = sidebar_filters(df)
dff = apply_filters(df, f)

st.title("Féminisation 2012 → 2023")

# agg / année
evol = dff.groupby(["nom_fed", "year"], as_index=False).agg(
    total_license=("total_lic", "sum"),
    total_f=("total_f", "sum")
)

evol["part_femmes"] = evol["total_f"] / evol["total_license"] * 100

# Parts en 2012 et 2022
p2012 = evol[evol["year"] == 2012][["nom_fed", "part_femmes"]].rename(
    columns={"part_femmes": "part_femmes_2012"}
)
p2023 = evol[evol["year"] == 2023][["nom_fed", "part_femmes"]].rename(
    columns={"part_femmes": "part_femmes_2023"}
)

evo = p2012.merge(p2023, on="nom_fed", how="inner")

# variation en points de %
evo["variation_absolue"] = evo["part_femmes_2023"] - evo["part_femmes_2012"]


lic_2023 = (
    dff[dff["year"] == 2023]
    .groupby("nom_fed", as_index=False)["total_lic"]
    .sum()
    .rename(columns={"total_lic": "licences_2023"})
)

evo = evo.merge(lic_2023, on="nom_fed", how="left")


# evolution feminisation
evo = evo.sort_values("variation_absolue", ascending=False)

# tableau top
top_n = st.slider("Top N", 5, 50, 20)
st.subheader(f"Top {top_n} fédérations — progression de la part des femmes (2012 - 2023)")

# (arrondi)
evo_display = evo.copy()
for col in ["part_femmes_2012", "part_femmes_2023", "variation_absolue"]:
    evo_display[col] = evo_display[col].round(2)

st.dataframe(evo_display.head(top_n), width="stretch")


#Série temporelle : évolution annuelle
st.subheader("Évolution annuelle (sélection)")
fed = st.selectbox("Choisir une fédération", sorted(evol["nom_fed"].unique()))
curve = evol[evol["nom_fed"] == fed].sort_values("year")

fig = px.line(
    curve,
    x="year",
    y="part_femmes",
    markers=True,
    title=f"Part des femmes — {fed}"
)
fig.update_layout(
    xaxis_title="Année",
    yaxis_title="Part des femmes (%)"
)

st.plotly_chart(fig, width="stretch")
