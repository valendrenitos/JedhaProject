import streamlit as st
import pandas as pd
import json
import plotly.express as px
import altair as alt

st.set_page_config(page_title="Licenciés sportifs par région", layout="wide")

# -------------------------------------------------------------------------
# -------------------------- CHARGEMENT DES DONNEES -----------------------
# -------------------------------------------------------------------------

@st.cache_data
def load_data():
    pop = pd.read_csv("data/pop_by_region.csv")  # reg_nom | population
    licenses = pd.read_csv("data/licenses_by_year_region_fed.csv")
    return pop, licenses

pop, licenses = load_data()

# ---- Charger GeoJSON des régions ----
with open("data/regions.geojson", "r", encoding="utf-8") as f:
    regions_geojson = json.load(f)

# -------------------------------------------------------------------------
# --------------------------- FILTRES SIDEBAR ------------------------------
# -------------------------------------------------------------------------

annees_dispo = sorted(licenses["annee"].unique())
annee_sel = st.sidebar.slider(
    "Sélectionner l'année",
    min_value=min(annees_dispo),
    max_value=max(annees_dispo),
    value=max(annees_dispo),
    step=1
)

fed_dispo = sorted(licenses["nom_fed"].unique())
fed_sel = st.sidebar.multiselect("Sélectionnez la ou les fédération(s)", fed_dispo)

# ---- Filtrage année + fédération ----
df_filtered = licenses[licenses["annee"] == annee_sel]

if fed_sel:
    df_filtered = df_filtered[df_filtered["nom_fed"].isin(fed_sel)]

# ---- Agrégation par région ----
df_region = df_filtered.groupby("region", as_index=False).agg({
    "total_license": "sum",
    "total_f": "sum",
    "total_h": "sum"
})

# ---- Merge avec population ----
df_region = df_region.merge(pop, left_on="region", right_on="reg_nom", how="left")

# ---- Calcul ratios ----
df_region["ratio_total"] = df_region["total_license"] / df_region["population"]
df_region["ratio_f"] = df_region["total_f"] / df_region["population"]

# -------------------------------------------------------------------------
# ----------------------------- KPI NATIONAUX ------------------------------
# -------------------------------------------------------------------------

# ---- Données année N ----
df_kpi_n = licenses[licenses["annee"] == annee_sel]

if fed_sel:
    df_kpi_n = df_kpi_n[df_kpi_n["nom_fed"].isin(fed_sel)]

# Agrégation nationale
total_lic_n = df_kpi_n["total_license"].sum()
total_f_n = df_kpi_n["total_f"].sum()

population_totale = pop["population"].sum()

ratio_n = total_lic_n / population_totale

# ---- Données année N-1 ----
df_kpi_n1 = licenses[licenses["annee"] == annee_sel - 1]

if fed_sel:
    df_kpi_n1 = df_kpi_n1[df_kpi_n1["nom_fed"].isin(fed_sel)]

total_lic_n1 = df_kpi_n1["total_license"].sum()
ratio_n1 = total_lic_n1 / population_totale

# ---- Évolution %
if ratio_n1 != 0:
    evolution_ratio = ((ratio_n - ratio_n1) / ratio_n1) * 100
else:
    evolution_ratio = 0

# ---- Part femmes
part_femmes = (total_f_n / total_lic_n) * 100 if total_lic_n != 0 else 0

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

st.subheader(f"Ratio licenciés / habitant par région - {annee_sel}")

fig_map = px.choropleth(
    df_region,
    geojson=regions_geojson,
    locations="region",
    featureidkey="properties.nom",  # à adapter selon ton geojson
    color="ratio_total",
    hover_name="region",
    color_continuous_scale="Viridis"
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

# -------------------------------------------------------------------------
# ------------------- ÉVOLUTION DES LICENCES PAR SEXE ---------------------
# -------------------------------------------------------------------------

st.subheader("Évolution des licences par sexe (France entière)")

df_evo = licenses.copy()

if fed_sel:
    df_evo = df_evo[df_evo["nom_fed"].isin(fed_sel)]

df_evo = df_evo.groupby("annee", as_index=False)[["total_f","total_h"]].sum()
df_evo = df_evo.melt(id_vars="annee", var_name="Sexe", value_name="Nombre de licences")

fig_line = alt.Chart(df_evo).mark_line(point=True).encode(
    x="annee:O",
    y="Nombre de licences:Q",
    color="Sexe:N",
    tooltip=["annee", "Sexe", "Nombre de licences"]
)

st.altair_chart(fig_line, use_container_width=True)

# -------------------------------------------------------------------------
# ----------------- EVOLUTION RATIO LICENCIES / HABITANT ------------------
# -------------------------------------------------------------------------

# ---- Année N ----
df_n = licenses[licenses["annee"] == annee_sel]

# ---- Année N-1 ----
df_n1 = licenses[licenses["annee"] == annee_sel - 1]

if fed_sel:
    df_n = df_n[df_n["nom_fed"].isin(fed_sel)]
    df_n1 = df_n1[df_n1["nom_fed"].isin(fed_sel)]

# ---- Agrégation région N ----
df_n = df_n.groupby("region", as_index=False).agg({
    "total_license": "sum",
    "total_f": "sum"
})

# ---- Agrégation région N-1 ----
df_n1 = df_n1.groupby("region", as_index=False).agg({
    "total_license": "sum",
    "total_f": "sum"
})

# ---- Merge population ----
df_n = df_n.merge(pop, left_on="region", right_on="reg_nom", how="left")
df_n1 = df_n1.merge(pop, left_on="region", right_on="reg_nom", how="left")

# ---- Calcul ratios ----
df_n["ratio_N"] = df_n["total_license"] / df_n["population"]
df_n["pct_femmes_actives"] = df_n["total_f"] / df_n["population"]

df_n1["ratio_N1"] = df_n1["total_license"] / df_n1["population"]
df_n1["pct_femmes_actives_N1"] = df_n1["total_f"] / df_n1["population"]

# ---- Merge N et N-1 ----
df_compare = df_n.merge(
    df_n1[["region", "ratio_N1", "pct_femmes_actives_N1"]],
    on="region",
    how="left"
)

# ---- Evolutions ----
df_compare["evolution_ratio_%"] = (
    (df_compare["ratio_N"] - df_compare["ratio_N1"])
    / df_compare["ratio_N1"] * 100
).round(2)

df_compare["evolution_femmes_%"] = (
    (df_compare["pct_femmes_actives"] - df_compare["pct_femmes_actives_N1"])
    / df_compare["pct_femmes_actives_N1"] * 100
).round(2)

# ---- Mise en forme finale ----
df_compare["% licenciés/habitant"] = (df_compare["ratio_N"] * 100).round(2)
df_compare["% femmes actives"] = (df_compare["pct_femmes_actives"] * 100).round(2)

# ---- Sélection colonnes finales ----
df_final = df_compare[[
    "region",
    "total_license",
    "population",
    "% licenciés/habitant",
    "evolution_ratio_%",
    "% femmes actives",
    "evolution_femmes_%"
]].rename(columns={
    "region": "Région",
    "total_license": "Total licenciés",
    "population": "Population",
    "evolution_ratio_%": f"% Evolution vs {annee_sel-1}",
    "evolution_femmes_%": "% Evolution femmes actives N-1"
})



st.subheader(f"Évolution du ratio licenciés / habitant - {annee_sel}")
st.dataframe(df_final)