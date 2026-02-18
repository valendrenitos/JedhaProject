import streamlit as st
import plotly.express as px
import pandas as pd
import app as mn
from utils import sidebar_filters, apply_filters

df = mn.data1

st.title("👩 Féminisation par fédération")

# Préparation des données
rolling_avg = (
    df.groupby(["nom_fed", "year"])["total_f"].sum() /
    df.groupby(["nom_fed", "year"])["total_lic"].sum()
).unstack("year").rolling(3, axis=1, min_periods=1).mean()

df_long = (
    rolling_avg
    .mul(100)
    .rename_axis("federation")
    .reset_index()
    .melt(id_vars="federation", var_name="annee", value_name="part_femmes")
)

df_long["progression"] = (
    df_long.groupby("federation")["part_femmes"]
    .transform(lambda s: s - s.iloc[0])
)

fig = px.scatter(
    df_long,
    x="part_femmes",
    y="progression",
    animation_frame="annee",
    animation_group="federation",
    hover_name="federation",
    labels={
        "part_femmes": "Part de femmes (%)",
        "progression": "Progression depuis l'origine (points de %)",
        "annee": "Année"
    },
    title="Évolution de la féminisation par fédération",
    height=750
)

fig.add_vline(x=50, line_dash="dash", line_color="red", opacity=0.5)
fig.add_hline(y=0, line_dash="dash", line_color="red", opacity=0.5)

fig.update_xaxes(range=[0, 100])
fig.update_yaxes(range=[-10, 35])

st.plotly_chart(fig, use_container_width=True)