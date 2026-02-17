import streamlit as st
import pandas as pd

def sidebar_filters(df: pd.DataFrame) -> dict:
    st.sidebar.header("Filtres")

    years = sorted(df["annee"].unique())
    year_min, year_max = st.sidebar.select_slider(
        "Période",
        options=years,
        value=(min(years), max(years))
    )

    regions = ["Toutes"] + sorted(df["region"].dropna().unique())
    region = st.sidebar.selectbox("Région", regions)

    feds = ["Toutes"] + sorted(df["nom_fed"].dropna().unique())
    fed = st.sidebar.selectbox("Fédération", feds)

    return {"year_min": year_min, "year_max": year_max, "region": region, "fed": fed}

def apply_filters(df: pd.DataFrame, f: dict) -> pd.DataFrame:
    out = df[(df["annee"] >= f["year_min"]) & (df["annee"] <= f["year_max"])].copy()
    if f["region"] != "Toutes":
        out = out[out["region"] == f["region"]]
    if f["fed"] != "Toutes":
        out = out[out["nom_fed"] == f["fed"]]
    return out

# CHAQUE PAGE FERA : df = lead_data() / f=sidebar_filter(df) / dff = apply_filters(df,f)