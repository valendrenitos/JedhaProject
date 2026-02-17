import streamlit as st
import pandas as pd
import numpy as np
import json

import plotly.express as px
import altair as alt

from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error, r2_score



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


# -------------------------------------------------------------------------
# ---------------------------- MACHINE LEARNING ---------------------------
# -------------------------------------------------------------------------

licenses["annee"] = licenses["annee"].astype(int)

# ------------------------------
# 2️⃣ Définir les features et target
# ------------------------------
features = [
    "annee",
    "region",
    "nom_fed",
    "total_license",
    "f_1_9", "f_10_19", "f_20_29", "f_30_59", "f_60_74", "f_75"
]
X = licenses[features]
y = licenses["total_f"]

categorical_cols = ["region", "nom_fed"]
numeric_cols = [col for col in features if col not in categorical_cols]

# Préprocessing
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
        ("num", "passthrough", numeric_cols)
    ]
)

# Pipeline Ridge
ridge_pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("model", Ridge(alpha=1.0))
])

# ------------------------------
# 3️⃣ Entraînement
# ------------------------------
ridge_pipeline.fit(X, y)

# ------------------------------
# 4️⃣ Streamlit UI : projections somme de toutes les fédérations
# ------------------------------

st.title("Projection des licences sportives féminines par région")
st.subheader("Ridge Regression")
st.markdown("Les projections sont calculées pour la somme de toutes les fédérations sélectionnées.")

regions = licenses["region"].unique()
selected_region = st.selectbox("Choisir une région :", regions)

# 1️⃣ Agrégation historique par région
df_hist = licenses[licenses["region"] == selected_region].copy()

if fed_sel:
    df_hist = df_hist[df_hist["nom_fed"].isin(fed_sel)]

df_hist_grouped = df_hist.groupby("annee")["total_f"].sum().reset_index()

# 2️⃣ Modèle Ridge simple sur l'année
X_train = df_hist_grouped[["annee"]]
y_train = df_hist_grouped["total_f"]

model_ridge_year = Ridge(alpha=1.0)
model_ridge_year.fit(X_train, y_train)

# 3️⃣ Projection 2024-2030
future_years = pd.DataFrame({"annee": np.arange(2024, 2031)})
future_pred = model_ridge_year.predict(future_years)
future_years["total_f"] = future_pred
future_years["type"] = "Projection"

# 4️⃣ Fusionner avec historique
df_plot = pd.concat([df_hist_grouped.assign(type="Historique"), future_years], ignore_index=True)

# ------------------------------
# 5️⃣ Visualisation interactive
# ------------------------------
fig = px.line(
    df_plot,
    x="annee",
    y="total_f",
    color="type",
    markers=True,
    title=f"Licences féminines - {selected_region} (Ridge Regression)"
)

fig.update_layout(
    xaxis_title="Année",
    yaxis_title="Nombre de licences féminines",
    template="plotly_white",
    yaxis=dict(tickformat=".2s")  # affiche 1k, 1M automatiquement
)

st.plotly_chart(fig, use_container_width=True)



# ------------------------------
# 2️⃣ Pipeline Ridge
# ------------------------------

ridge_pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("model", Ridge(alpha=1.0))  # alpha = force de régularisation
])

# Split temporel simple : années <=2021 pour train, >2021 pour test
X_train = X[licenses["annee"] <= 2021]
X_test  = X[licenses["annee"] > 2021]
y_train = y[licenses["annee"] <= 2021]
y_test  = y[licenses["annee"] > 2021]

# Entraînement
ridge_pipeline.fit(X_train, y_train)

# ------------------------------
# 3️⃣ Évaluation
# ------------------------------

y_pred = ridge_pipeline.predict(X_test)

rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

## Interprétation des scores

st.subheader(f"R2 score: {round(r2,4)}")

st.markdown('''
- ≈ 71 % de la variance expliquée par le modèle. 
- Comparé à 0.36 avant, ça veut dire que le modèle Ridge capture beaucoup mieux la tendance des licences féminines. 
- En clair : les variables utilisées (année + région + fédération + tranches d’âge + total_license) expliquent la majorité des variations.
''')

st.subheader(f"RMSE du modèle: {round(rmse)}")

st.markdown('''
- RMSE est l’erreur moyenne en valeur absolue (racine de l’erreur quadratique). 
- Donc, en moyenne, le modèle se trompe de ~4 500 licences par région/fédération par an. 
- Si les effectifs par fédération sont de l’ordre de 50 000 à 200 000 licences, l’erreur relative est très faible (<10%). 

💡 En résumé : c’est un modèle robuste et précis, bien meilleur que le modèle simple basé seulement sur l’année.
''')