import streamlit as st
import pandas as pd
import plotly.express as px
import app as mn
import plotly.graph_objects as go

df =mn.data2
df.loc[(
    df["sport_event"]=="Roland Garros") & (df["year"]==2016),
    "genre"] = "mixte"


print(df)

data_pie = df.groupby("genre", as_index=False)["avrg_tv_aud"].sum()

color_map = {
    "féminin": "#f59a53",
    "masculin": "#0e1f3a",
    "mixte": "#5a815c"
}

fig_target = go.Figure(data=[go.Pie(labels=data_pie["genre"],
                                     values=data_pie["avrg_tv_aud"],
                                     hole=.3,
                                     marker=dict(
                colors=[color_map[g] for g in data_pie["genre"]])
                                 )])

st.plotly_chart(fig_target, use_container_width=True)