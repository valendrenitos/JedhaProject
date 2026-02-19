import streamlit as st
import pandas as pd
import plotly.express as px
import app as mn
import plotly.graph_objects as go

df =mn.data2

print(df.head())

fig_target = go.Figure(data=[go.Pie(labels=df["genre"].unique(),
                                     values=df.groupby(['genre'])["avrg_tv_aud"].sum(),
                                     hole=.3)])

st.plotly_chart(fig_target, use_container_width=True)