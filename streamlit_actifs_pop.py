import streamlit as st
import pandas as pd
import json
import plotly.express as px
import altair as alt

st.set_page_config(page_title="Licenciés sportifs par département", layout="wide")

# -------------------------------------------------------------------------
# -------------------------- CHARGEMENT DES DONNEES -----------------------
# -------------------------------------------------------------------------

# ---- Charger les données ----
@st.cache_data
def load_data():
    df = pd.read_csv("data/ratio_actifs_habitants_dpt.csv")
    df["num_departement"] = df["num_departement"].astype(str).str.zfill(2)
    return df
df = load_data()

# ---- Charger GeoJSON des départements ----
with open("data/departements.geojson", "r", encoding="utf-8") as f:
    departements_geojson = json.load(f)

# -------------------------------------------------------------------------
# --------------------------- FILTRES DE GAUCHE --------------------------
# -------------------------------------------------------------------------

# ---- Sélection de l'année ----
annees_dispo = sorted(df["annee"].unique())
annee_sel = st.sidebar.slider("Sélectionner l'année", min_value=min(annees_dispo),
                              max_value=max(annees_dispo), value=max(annees_dispo), step=1)

df_annee = df[df["annee"] == annee_sel]

# ---- Sélection de la fédération ----
fed_dispo = sorted(df["nom_fed"].unique())
fed_sel = st.sidebar.multiselect("Sélectionnez la ou les fédération",options=fed_dispo)
# Si aucune fédération n'est sélectionnée, on prend toutes
if fed_sel:
    df_annee = df_annee[df_annee["nom_fed"].isin(fed_sel)]

# -------------------------------------------------------------------------
# ---------------------------------- CARTE --------------------------------
# -------------------------------------------------------------------------

# ---- Carte choroplèthe ratio licenciés/habitant ----
st.subheader(f"Ratio licenciés/habitant par département - {annee_sel}")

fig_map = px.choropleth(
    df_annee,
    geojson=departements_geojson,
    locations='num_departement',
    color='ratio_lic_hab',
    hover_name='dep_nom',
    color_continuous_scale="Viridis",
    featureidkey="properties.code"
)
fig_map.update_geos(fitbounds="locations", visible=False)
fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig_map, use_container_width=True)

# -------------------------------------------------------------------------
# ------------- Top 10 départements par nombre de licenciés ---------------
# -------------------------------------------------------------------------

# ---- Top 10 départements par nombre de licenciés ----
st.subheader(f"Top 10 départements par nombre de licenciés - {annee_sel}")
top10 = df_annee.nlargest(10, "licences")

fig_bar = alt.Chart(top10).mark_bar().encode(
    x=alt.X("licences:Q", title="Nombre de licenciés"),
    y=alt.Y("dep_nom:N", sort='-x', title="Département"),
    tooltip=["dep_nom", "licences", "total_f", "total_h"]
).properties(height=400)
st.altair_chart(fig_bar, use_container_width=True)

# -------------------------------------------------------------------------
# ------------------- Évolution des licences par sexe --------------------
# -------------------------------------------------------------------------

# ---- Évolution des licences par sexe sur toutes les années ----
st.subheader("Évolution des licences par sexe")

df_evo = df.groupby("annee", as_index=False)[["total_f","total_h"]].sum()
df_evo = df_evo.melt(id_vars="annee", var_name="Sexe", value_name="Nombre de licences")

fig_line = alt.Chart(df_evo).mark_line(point=True).encode(
    x="annee:O",
    y="Nombre de licences:Q",
    color="Sexe:N",
    tooltip=["annee", "Sexe", "Nombre de licences"]
)
st.altair_chart(fig_line, use_container_width=True)

# -------------------------------------------------------------------------
# ----------------- EVOLUTION DE LICENCIES PAR HABITANT -------------------
# -------------------------------------------------------------------------

# ---- Filtrer pour N et N-1 en utilisant df_annee (année + fédération) ----
df_n = df_annee.groupby("dep_nom", as_index=False).agg(
    ratio_lic_hab_N=("ratio_lic_hab", "sum")  # moyenne par département
)

df_n_1 = df[(df["annee"] == annee_sel - 1)]  # année N-1, mais on peut filtrer sur les mêmes fédérations
if fed_sel:
    df_n_1 = df_n_1[df_n_1["nom_fed"].isin(fed_sel)]
df_n_1 = df_n_1.groupby("dep_nom", as_index=False).agg(
    ratio_lic_hab_N_1=("ratio_lic_hab", "sum")
)

# ---- Merge et calcul évolution ----
df_compare = pd.merge(df_n, df_n_1, on="dep_nom", how="left")
df_compare["evolution_%"] = ((df_compare["ratio_lic_hab_N"] - df_compare["ratio_lic_hab_N_1"]) 
                             / df_compare["ratio_lic_hab_N_1"] * 100).round(2)

# ---- Préparer le tableau final ----
df_table = df_compare.rename(columns={
    "dep_nom": "Département",
    "ratio_lic_hab_N": f"% licenciés/habitant {annee_sel}",
    "ratio_lic_hab_N_1": "% Licenciés par habitant N-1",
    "evolution_%": f"Évolution % par rapport à {annee_sel-1}"
})

# ---- Formater les valeurs en % ----
df_table[f"% licenciés/habitant {annee_sel}"] = (df_table[f"% licenciés/habitant {annee_sel}"].astype(float)*100).round(2)
df_table["% Licenciés par habitant N-1"] = (df_table["% Licenciés par habitant N-1"].astype(float)*100).round(2)
df_table[f"Évolution % par rapport à {annee_sel-1}"] = df_table[f"Évolution % par rapport à {annee_sel-1}"].astype(float).round(2)

st.subheader(f"Évolution du ratio de licenciés par habitant - {annee_sel}")
st.dataframe(df_table)

# -------------------------------------------------------------------------
# ----------- EVOLUTION DE LICENCIES FEMMES PAR HABITANT ---------
# -------------------------------------------------------------------------

# ---- Même chose pour les femmes ----
df_f_n = df_annee.groupby("dep_nom", as_index=False).agg(
    ratio_lic_hab_f_N=("ratio_lic_f_hab", "sum")
)

df_f_n_1 = df[(df["annee"] == annee_sel - 1)]
if fed_sel:
    df_f_n_1 = df_f_n_1[df_f_n_1["nom_fed"].isin(fed_sel)]
df_f_n_1 = df_f_n_1.groupby("dep_nom", as_index=False).agg(
    ratio_lic_hab_f_N_1=("ratio_lic_f_hab", "sum")
)

df_f_compare = pd.merge(df_f_n, df_f_n_1, on="dep_nom", how="left")
df_f_compare["evolution_%"] = ((df_f_compare["ratio_lic_hab_f_N"] - df_f_compare["ratio_lic_hab_f_N_1"])/df_f_compare["ratio_lic_hab_f_N_1"]*100).round(2)

df_f_table = df_f_compare.rename(columns={
    "dep_nom": "Département",
    "ratio_lic_hab_f_N": f"% licenciés femmes/habitant {annee_sel}",
    "ratio_lic_hab_f_N_1": "% Licenciés femmes par habitant N-1",
    "evolution_%": f"Évolution % par rapport à {annee_sel-1}"
})

df_f_table[f"% licenciés femmes/habitant {annee_sel}"] = (df_f_table[f"% licenciés femmes/habitant {annee_sel}"].astype(float)*100).round(2)
df_f_table["% Licenciés femmes par habitant N-1"] = (df_f_table["% Licenciés femmes par habitant N-1"].astype(float)*100).round(2)
df_f_table[f"Évolution % par rapport à {annee_sel-1}"] = df_f_table[f"Évolution % par rapport à {annee_sel-1}"].astype(float).round(2)

st.subheader(f"Évolution du ratio de licenciés femmes par habitant - {annee_sel}")
st.dataframe(df_f_table)