import streamlit as st
import pandas as pd
import plotly.express as px
import app as mn
import plotly.graph_objects as go

df =mn.data2
#### histo top 15
f_for_rank = dict(f)
f_for_rank["region"] = "Toutes"

dff = apply_filters(df, f_for_rank)

st.title(" Analyse régions")

metric = st.selectbox("Indicateur", ["total_lic", "total_h", "total_f"])
top_n = st.slider("Top N régions", 5, 30, 18)

by_region = dff.groupby("region")[metric].sum().sort_values(ascending=False)
total_nat = by_region.sum()

rank = by_region.reset_index().rename(columns={metric: "Total"})
rank["Part (%)"] = (rank["Total"] / total_nat * 100).round(2)

st.dataframe(rank, use_container_width=True)

fig_histo = px.bar(rank.head(top_n).sort_values("Total"), x="Total", y="region", orientation="h",
             title=f"Top {top_n} régions — {metric}")
st.plotly_chart(fig_histo, use_container_width=True)

