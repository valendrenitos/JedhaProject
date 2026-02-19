import streamlit as st
import pandas as pd
import plotly.express as px
import app as mn
from utils import sidebar_filters, apply_filters

df = mn.data1
f = sidebar_filters(df)
dff = apply_filters(df, f)

st.title("Analyse par fédération sportive")

# controle
col1, col2, col3 = st.columns(3)

with col1:
    années = sorted(dff["year"].unique())
    année_choisie = st.selectbox(" Année", années)

with col2:
    metric = st.selectbox(" Indicateur", {
        "total_lic": "Total licenciés",
        "total_h":   "Hommes",
        "total_f":   "Femmes",
    }.keys(), format_func=lambda x: {
        "total_lic": "Total licenciés",
        "total_h":   "Hommes",
        "total_f":   "Femmes",
    }[x])

with col3:
    top_n = st.slider(" Top N fédérations", 5, 50, 15)

dff_year = dff[dff["year"] == année_choisie]

# calculs
by_fed = dff_year.groupby("nom_fed")[metric].sum().sort_values(ascending=False)
total_global = by_fed.sum()
top3_share= by_fed.head(3).sum() / total_global * 100 if total_global else 0
top1_fed = by_fed.index[0] if len(by_fed) > 0 else "—"
nb_feds = len(by_fed)

# kpi
k1, k2, k3, k4 = st.columns(4)
k1.metric(" Total licenciés", f"{total_global:,.0f}")
k2.metric(" N°1", top1_fed)
k3.metric(" Part du Top 3", f"{top3_share:.1f}%")

st.divider()

# graph
table = by_fed.reset_index().rename(columns={metric: "Total"})

fig = px.bar(
    table.head(top_n).sort_values("Total"),
    x="Total", y="nom_fed", orientation="h",
    title=f"Top {top_n} fédérations — {année_choisie}",
    labels={"nom_fed": "Fédération", "Total": "Licenciés"},
    text_auto=".2s",
)
fig.update_layout(yaxis_title="", xaxis_title="Licenciés")
st.plotly_chart(fig, use_container_width=True)

# tableau
with st.expander(" Voir le tableau complet"):
    table["% du total"] = (table["Total"] / total_global * 100).round(1).astype(str) + "%"
    st.dataframe(table, use_container_width=True, hide_index=True)