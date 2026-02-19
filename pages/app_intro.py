import pandas as pd
import streamlit as st 
import plotly.express as px 
import plotly.graph_objects as go
import numpy as np
from utils import sidebar_filters, apply_filters
import app as mn
import json

# Test d'aller chercher les modules dans les fichiers de Sky
#from JedhaProject.streamlit_graphs import graph_comparaison_media_lic as stg
#from JedhaProject.pages.vue_ensemble import show_vue_ensemble
#from JedhaProject.utils import sidebar_filters

from DBConnector import getData

df = mn.data1
f = sidebar_filters(df)
dff = apply_filters(df, f)


# DATA 1 : LICENSES : COLONNES : year,  region,  nom_fed, total_lic, total_f, total_h, h_1_9, h_10_19, h_20_29,h_30_59,h_60_74, h_75, f_1_9, f_10_19, f_20_29, f_30_59, f_60_74, f_75
# DATA 2 : Medias : sport_event,sport,year,avrg_tv_aud,avrg_tv_match,total_match,hours_live,numb_of_post
# DATA 3 Club 49-23 : annee,  olympics,  non_olympics, affinitaire, scholair, total

st.subheader("Problématique")

st.markdown("""
    Mettre la problématique ici
""")

def show_vue_ensemble():
    st.title("📊 Vue d’ensemble")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Période", f"{dff['year'].min()} → {dff['year'].max()}")
    c2.metric("Observations", f"{len(dff):,}".replace(",", " "))
    c3.metric("Régions", dff["region"].nunique())
    c4.metric("Fédérations", dff["nom_fed"].nunique())

    st.subheader("Aperçu des données")
    st.dataframe(dff.head(50), use_container_width=True)

show_vue_ensemble()

# ---- Charger GeoJSON des régions ----
with open("data/regions.geojson", "r", encoding="utf-8") as f:
    regions_geojson = json.load(f)

# -------------------------------------------------------------------------
# ----------------------------- KPI NATIONAUX ------------------------------
# -------------------------------------------------------------------------
total_lic_n = 


st.title("KPI Nationaux")
c1, c2, c3, c4 = st.columns(4)

c2.metric(
    label="Total licenciés",
    value=f"{int(total_lic_n):,}".replace(",", " ")
)



# -------------------------------------------------------------------------
# ------------------------------ AFFICHAGE KPI -----------------------------
# -------------------------------------------------------------------------

st.markdown("## 📊 Indicateurs nationaux")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    label=f"Ratio licenciés / habitant ({annee_sel})",
    value=f"{ratio_n*100:.2f}%",
    delta=f"{evolution_ratio:.2f}% vs {annee_sel-1}"
)

col2.metric(
    label="Total licenciés",
    value=f"{int(total_lic_n):,}".replace(",", " ")
)

col3.metric(
    label="Part des femmes",
    value=f"{part_femmes:.2f}%"
)

col4.metric(
    label="Population totale",
    value=f"{int(population_totale):,}".replace(",", " ")
)

# -------------------------------------------------------------------------
# ---------------------------------- CARTE --------------------------------
# -------------------------------------------------------------------------

# mini = 
# maxi = 

st.subheader(f"Ratio licenciés / habitant par région - {annee_sel}")

fig_map = px.choropleth(
    df_region,
    geojson=regions_geojson,
    locations="region",
    featureidkey="properties.nom",  # à adapter selon ton geojson
    color="ratio_total",
    hover_name="region",
    color_continuous_scale="Viridis",
    #range_color=[mini, maxi]
)

fig_map.update_geos(fitbounds="locations", visible=False)
fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

st.plotly_chart(fig_map, use_container_width=True)


# -------------------------------------------------------------------------
# ----------------------- TOP 10 REGIONS ----------------------------------
# -------------------------------------------------------------------------

st.subheader(f"Top régions par nombre de licenciés - {annee_sel}")

top_regions = df_region.sort_values("total_license", ascending=False)

fig_bar = alt.Chart(top_regions).mark_bar().encode(
    x=alt.X("total_license:Q", title="Nombre de licenciés"),
    y=alt.Y("region:N", sort='-x', title="Région"),
    tooltip=["region", "total_license", "total_f", "total_h"]
).properties(height=400)

st.altair_chart(fig_bar, use_container_width=True)