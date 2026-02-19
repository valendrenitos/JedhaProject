import streamlit as st
import pandas as pd
import plotly.express as px
import app as mn

df =mn.data1



df_grouped = df.groupby(['nom_fed','year'], as_index=False)['total_lic'].sum()

df_grouped = df_grouped.sort_values(['nom_fed','year'])

df_grouped['progression_pct'] = (
    df_grouped.groupby('nom_fed')['total_lic']
              .pct_change() 
              *100
)


fig = px.scatter(
    df_grouped,
    x="total_lic",
    y="progression_pct",
    animation_frame="year",
    animation_group="nom_fed",
    hover_name="nom_fed",
    labels={
        "total lics": "Total licenciés",
        "progression_pct": "Progression depuis l'origine",
        "year": "Année"
    },
    title="Évolution des licenciés par fédération",
    height=750
)

fig.add_vline(x=50, line_dash="dash", line_color="red", opacity=0.5)
fig.add_hline(y=0, line_dash="dash", line_color="red", opacity=0.5)

fig.update_xaxes(range=[df_grouped["total_lic"].min(), df_grouped["total_lic"].max()])
fig.update_yaxes(range=[-35,35])

st.plotly_chart(fig, use_container_width=True)