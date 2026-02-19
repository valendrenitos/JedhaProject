import streamlit as st
import plotly.express as px
import pandas as pd
import app as mn
from utils import sidebar_filters, apply_filters

df = mn.data1

st.title("👩 Féminisation par fédération")


# Récupérer les années qu'on veut 
annees = sorted(df_long["annee"].unique())

# Sélecteur d'année
annee_selectionnee = st.selectbox("Sélectionnez une année", annees)

# Dictionnaire des textes par année
textes_par_annee = {
    2015: "texte",
    2016: "texte",
    2017: "On est en 2017 ",
}


# Bouton
texte_defaut = "Aucune analyse disponible pour cette année."
if st.button("Afficher l'analyse"):
    st.write(textes_par_annee.get(annee_selectionnee, texte_defaut))
else:
    st.info("Sélectionnez une année puis cliquez sur le bouton.")