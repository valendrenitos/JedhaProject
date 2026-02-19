import streamlit as st
import pandas as pd
import plotly.express as px
import app as mn

df =mn.data1


rolling_avg = (
   df.groupby(["year", "nom_fed"])["total_lic"].sum()
).unstack("year").rolling(3, axis=1, min_periods=1).mean()

df_long = (
    rolling_avg
    .mul(100)
    .rename_axis("federation")
    .reset_index()
    .melt(id_vars="federation", var_name="annee", value_name="total_lic")
)

df_long["progression"] = (
    df_long.groupby("federation")["total_lic"]
    .transform(lambda s: s - s.iloc[0])
)

print(df_long[df_long["annee"]==2020])

fig = px.scatter(
    df_long,
    x="total_lic",
    y="progression",
    animation_frame="annee",
    animation_group="federation",
    hover_name="federation",
    labels={
        "total lics": "Total licenciés",
        "progression": "Progression depuis l'origine",
        "annee": "Année"
    },
    title="Évolution des licenciés par fédération",
    height=750
)

fig.add_vline(x=50, line_dash="dash", line_color="red", opacity=0.5)
fig.add_hline(y=0, line_dash="dash", line_color="red", opacity=0.5)

fig.update_xaxes(range=[df["total_lic"].min(), df["total_lic"].max()])
fig.update_yaxes(range=[-10, 35])

st.plotly_chart(fig, use_container_width=True)