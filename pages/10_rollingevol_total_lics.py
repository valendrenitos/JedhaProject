import streamlit as st
import pandas as pd
import plotly.express as px
import app as mn

df =mn.data1


rolling_avg = (
<<<<<<< HEAD
   df.groupby(["year", "nom_fed"])["total_lic"].sum()
=======
    df.groupby(["year","nom_fed" ])["total_lic"].sum()
>>>>>>> b9176fca397dabdae50c68861b0818e957dd05d2
).unstack("year").rolling(3, axis=1, min_periods=1).mean()

df=df.groupby(['nom_fed','year'], as_index=False).agg(total_lic=('total_lic','sum'))

df['total_lic_rolling3'] = df['total_lic'].rolling(window=3).mean()
print(df.head(50))
df_long = (
    rolling_avg
    .rename_axis("federation")
    .reset_index()
<<<<<<< HEAD
    .melt(id_vars="federation", var_name="annee", value_name="total_lic")
=======
    .melt(id_vars="federation", var_name="annee", value_name="total_lics")
>>>>>>> b9176fca397dabdae50c68861b0818e957dd05d2
)
print(df_long.head(50))

df_long["progression"] = (
    df_long.groupby(["federation","annee"])["total_lics"]
    .transform(lambda s: s - s.iloc[0])
)
<<<<<<< HEAD

print(df_long[df_long["annee"]==2020])

fig = px.scatter(
    df_long,
    x="total_lic",
=======
df_long.info()
print(df_long.head(20))
fig = px.scatter(
    df_long,
    x="total_lics",
>>>>>>> b9176fca397dabdae50c68861b0818e957dd05d2
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

<<<<<<< HEAD
fig.update_xaxes(range=[df["total_lic"].min(), df["total_lic"].max()])
fig.update_yaxes(range=[-10, 35])
=======
fig.update_xaxes(range=[0, max(df_long["total_lics"])])
fig.update_yaxes(range=[-1000, 1000])
>>>>>>> b9176fca397dabdae50c68861b0818e957dd05d2

st.plotly_chart(fig, use_container_width=True)