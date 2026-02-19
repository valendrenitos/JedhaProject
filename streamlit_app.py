import pandas as pd
import streamlit as st 
import plotly.express as px 
import plotly.graph_objects as go
import numpy as np
import streamlit_graphs as stg
from DBConnector import getData




st.set_page_config(
    page_title="Projet Final jedha DAFS-16",
    page_icon="💸 ",
    layout="wide"
)

with st.sidebar:
    st.page_link("streamlit_app.py", label="Accueil", icon="🏠")
    st.page_link("pages/1_Vue_ensemble.py", label="Vue d'ensemble du sport en France", icon="💪")
    st.page_link("pages/2_Analyse_temporelle.py", label="Analyse temporelle du sport en France", icon="📈")
    st.page_link("pages/3_Analyse_sexe.py", label="Sport & Femmes : Les médias comme levier ?", icon="♀️")
    st.page_link("pages/4_Annexes.py", label="Annexes ", icon="📋")





@st.cache_data
def load_data():
    data1,data2,data3,data4=getData()   
    return data1,data2,data3,data4

data1,data2,data3,data4=load_data()
data3.loc[(data3["annee"] >= 2016) & (data3["annee"] <= 2024), "total"] /= 2.6


# DATA 1 : LICENSES : COLONNES : year,  region,  nom_fed, total_lic, total_f, total_h, h_1_9, h_10_19, h_20_29,h_30_59,h_60_74, h_75, f_1_9, f_10_19, f_20_29, f_30_59, f_60_74, f_75
# DATA 2 : Medias : sport_event,sport,year,avrg_tv_aud,avrg_tv_match,total_match,hours_live,numb_of_post,genre
# DATA 3 Club 49-23 : annee,  olympics,  non_olympics, affinitaire, scholair, total
# DATA 4 rec : annee , reg, pop
st.subheader("Problématique")

st.markdown("""
    Mettre la problématique ici
""")

# APPELER LA FONCTION PERMETTANT LA GEN DU GRAPH EN DESSOUS ####
# NOM_VARIABLE_FILTRE= st.multiselect("CHOISIR LE TITRE DU FILTRE", 
#                               DATA_A_FILTRER["FILTRE"].sort_values().unique(), 
#                               placeholder=None,
#                               label_visibility="visible", 
#                               accept_new_options=False, 
#                               width="stretch")

# RAJOUTER LA FONCTION SOUS LA FORME 
# NOM_GRAPH = stg.NOM_DE_LA_FONCTION(VOS_VARIABLES)


# AJOUTER st.plotly_chart( VOTRE_GRAPH, use_container_width='stretch') en dessous

