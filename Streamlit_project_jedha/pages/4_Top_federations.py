import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    return pd.read_csv("data/licenses_by_year_region_fed.csv")

from utils import sidebar_filters, apply_filters

df = load_data()
f = sidebar_filters(df)
dff = apply_filters(df, f)

st.title("🏆 Analyse par fédération")

metric = st.selectbox("Indicateur", ["total_license", "total_h", "total_f"])
top_n = st.slider("Top N", 5, 50, 15)

by_fed = dff.groupby("nom_fed")[metric].sum().sort_values(ascending=False)
total_global = by_fed.sum()
top3_share = (by_fed.head(3).sum() / total_global * 100) if total_global else 0

st.metric("Part du Top 3 (%)", f"{top3_share:.1f}")

table = by_fed.reset_index().rename(columns={metric: "total"})
st.dataframe(table.head(50), use_container_width=True)

fig = px.bar(
    table.head(top_n).sort_values("total"),
    x="total", y="nom_fed", orientation="h",
    title=f"Top {top_n} fédérations — {metric}"
)
st.plotly_chart(fig, use_container_width=True)
