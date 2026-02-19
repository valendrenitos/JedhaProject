import streamlit as st
import pandas as pd
import plotly.express as px
import app as mn
from utils import sidebar_filters, apply_filters

df = mn.data1
f = sidebar_filters(df)
dff = apply_filters(df, f)

st.title(" Féminisation des fédérations sportives")

# anneés 
années_dispo = sorted(dff["year"].unique())
année_debut  = années_dispo[0]
année_fin    = années_dispo[-1]

st.caption(f"Analyse de l'évolution de la part des femmes — {année_debut} → {année_fin}")
st.divider()

# agg anne fed
evol = dff.groupby(["nom_fed", "year"], as_index=False).agg(
    total_lic=("total_lic", "sum"),
    total_f=("total_f", "sum"),
)
evol["part_femmes"] = evol["total_f"] / evol["total_lic"] * 100

# 2012 - 2023
p_debut = (
    evol[evol["year"] == année_debut][["nom_fed", "part_femmes"]]
    .rename(columns={"part_femmes": f"part_{année_debut}"})
)
p_fin = (
    evol[evol["year"] == année_fin][["nom_fed", "part_femmes"]]
    .rename(columns={"part_femmes":f"part_{année_fin}"})
)

evo = p_debut.merge(p_fin, on="nom_fed", how="inner")
evo["variation (pts)"] = evo[f"part_{année_fin}"] - evo[f"part_{année_debut}"]

# Licences fin de période
lic_fin = (
    dff[dff["year"] == année_fin]
    .groupby("nom_fed", as_index=False)["total_lic"]
    .sum()
    .rename(columns={"total_lic": f"licences_{année_fin}"})
)
evo = evo.merge(lic_fin, on="nom_fed", how="left")
evo = evo.sort_values("variation (pts)", ascending=False)

# kpi
part_globale_debut = (
    dff[dff["year"] == année_debut]["total_f"].sum()
    / dff[dff["year"] == année_debut]["total_lic"].sum() * 100
)
part_globale_fin = (
    dff[dff["year"] == année_fin]["total_f"].sum()
    / dff[dff["year"] == année_fin]["total_lic"].sum() * 100
)
top_progresseur  = evo.iloc[0]["nom_fed"] if len(evo) > 0 else "—"
top_regresseur   = evo.iloc[-1]["nom_fed"] if len(evo) > 0 else "—"

k1, k2, k3, k4 = st.columns(4)
k1.metric(f"♀️ Part femmes {année_debut}", f"{part_globale_debut:.1f}%")
k2.metric(f"♀️ Part femmes {année_fin}",   f"{part_globale_fin:.1f}%")


st.divider()

# Tableau
col_ctrl1, col_ctrl2 = st.columns([2, 3])
with col_ctrl1:
    top_n = st.slider("Top N fédérations", 5, 50, 20)
with col_ctrl2:
    sens = st.radio("Trier par", ["Plus grande progression", "Plus grande régression"],
                    horizontal=True)

evo_sorted = evo if sens == "Plus grande progression" else evo.sort_values("variation (pts)")

st.subheader(f"Top {top_n} — {sens} ({année_debut} → {année_fin})")

evo_display = evo_sorted.head(top_n).copy()
for col in [f"part_{année_debut}", f"part_{année_fin}", "variation (pts)"]:
    evo_display[col] = evo_display[col].round(1)

st.dataframe(evo_display, use_container_width=True, hide_index=True)

st.divider()

# graph
st.subheader(f"Variation de la part des femmes par fédération ({année_debut} → {année_fin})")

fig_bar = px.bar(
    evo_sorted.head(top_n).sort_values("variation (pts)"),
    x="variation (pts)", y="nom_fed", orientation="h",
    text_auto=".1f",
    labels={"nom_fed": "Fédération"},
    color="variation (pts)",
    color_continuous_scale="RdYlGn",
    color_continuous_midpoint=0,
)
fig_bar.update_layout(
    yaxis_title="",
    xaxis_title="Variation (points de %)",
    coloraxis_showscale=False,
)
st.plotly_chart(fig_bar, use_container_width=True)

st.divider()

# courbe par federation
st.subheader("Évolution annuelle par fédération")

col_fed, col_ref = st.columns([3, 2])
with col_fed:
    fed = st.selectbox("Choisir une fédération", sorted(evol["nom_fed"].unique()))
with col_ref:
    show_moyenne = st.toggle("Afficher la moyenne générale", value=True)

curve = evol[evol["nom_fed"] == fed].sort_values("year")

fig_line = px.line(
    curve, x="year", y="part_femmes",
    markers=True,
    title=f"Part des femmes — {fed}",
    labels={"year": "Année", "part_femmes": "Part des femmes (%)"},
)

if show_moyenne:
    moyenne_annuelle = evol.groupby("year")["part_femmes"].mean().reset_index()
    fig_line.add_scatter(
        x=moyenne_annuelle["year"],
        y=moyenne_annuelle["part_femmes"],
        mode="lines",
        name="Moyenne toutes fédérations",
        line=dict(dash="dash"),
    )

fig_line.update_layout(
    xaxis_title="Année",
    yaxis_title="Part des femmes (%)",
    yaxis=dict(range=[0, 100]),
)
st.plotly_chart(fig_line, use_container_width=True)