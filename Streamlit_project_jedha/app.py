import streamlit as st
import pandas as pd

st.set_page_config(page_title="EDA Licences Sportives", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("data/licenses_by_year_region_fed.csv")

df = load_data()

st.title("Analyse Exploratoire — Licences sportives (2012–2023)")
st.markdown("""
Cette application reprend le notebook EDA et ajoute de l’interactivité :
- filtres par **année**, **région**, **fédération**
- graphiques interactifs
- tableaux triables
""")

st.info("👉 Utilise le menu à gauche (pages) pour naviguer dans l’exposé.")
