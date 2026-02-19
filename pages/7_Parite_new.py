import streamlit as st
import pandas as pd
import plotly.express as px
import app as mn
from utils import sidebar_filters, apply_filters

df = mn.data1
f = sidebar_filters(df)
dff = apply_filters(df, f)

st.title(" Parité dans les fédérations sportives")
st.divider()

# controleurs
col1, col2 = st.columns(2)
with col1:
    années = sorted(dff["year"].unique())
    année_choisie = st.selectbox(" Année", années)
with col2:
    min_total = st.slider("Seuil minimal de licences", 0, 200000, 10000, step=1000)

dff_year = dff[dff["year"] == année_choisie]

# calcules
parite = dff_year.groupby("nom_fed", as_index=False).agg(
    total_lic=("total_lic", "sum"),
    total_f=("total_f", "sum"),
    total_h=("total_h", "sum"),
)
parite["part_femmes"] = (parite["total_f"] / parite["total_lic"] * 100).round(1)
parite = parite[parite["total_lic"] >= min_total].sort_values("part_femmes", ascending=False)

# kpi
nb_paritaires = ((parite["part_femmes"] >= 45) & (parite["part_femmes"] <= 55)).sum()
part_moy = parite["part_femmes"].mean()
plus_fem  = parite.iloc[0]["nom_fed"]  if len(parite) > 0 else "—"
moins_fem = parite.iloc[-1]["nom_fed"] if len(parite) > 0 else "—"

k1, k2, k3, k4 = st.columns(4)
k1.metric(" Fédérations analysées", len(parite))
k2.metric(" Part femmes moyenne", f"{part_moy:.1f}%")
k3.metric(" Plus féminisée",plus_fem)
k4.metric(" Moins féminisée", moins_fem)

st.divider()

# Top 10 plus / moins féminisées
cols = ["nom_fed", "part_femmes", "total_lic"]
col_labels = {"nom_fed": "Fédération", "part_femmes": "% Femmes", "total_lic": "Licences"}

c1, c2 = st.columns(2)
with c1:
    st.subheader(" Top 10 — plus féminisées")
    st.dataframe(
        parite.head(10)[cols].rename(columns=col_labels),
        use_container_width=True, hide_index=True,
    )
with c2:
    st.subheader(" Top 10 — moins féminisées")
    st.dataframe(
        parite.tail(10).sort_values("part_femmes")[cols].rename(columns=col_labels),
        use_container_width=True, hide_index=True,
    )

st.divider()

# histo
st.subheader("Distribution de la part des femmes")

fig = px.histogram(
    parite, x="part_femmes", nbins=30,
    title=f"Répartition des fédérations par part des femmes — {année_choisie}",
    labels={"part_femmes": "Part des femmes (%)"},
)
fig.add_vline(x=50, line_dash="dash", annotation_text="Parité (50%)", annotation_position="top right")
fig.add_vline(x=part_moy, line_dash="dot", annotation_text=f"Moyenne ({part_moy:.1f}%)", annotation_position="top left")
fig.update_layout(bargap=0.1, xaxis_range=[0, 100])
st.plotly_chart(fig, use_container_width=True)

# splatter
st.subheader("Taille vs féminisation")

fig2 = px.scatter(
    parite, x="total_lic", y="part_femmes",
    hover_name="nom_fed",
    labels={"total_lic": "Nombre de licences", "part_femmes": "Part des femmes (%)"},
    title="Nombre de licences vs part des femmes",
    size="total_lic", size_max=40,
)
fig2.add_hline(y=50, line_dash="dash", annotation_text="Parité")
st.plotly_chart(fig2, use_container_width=True)