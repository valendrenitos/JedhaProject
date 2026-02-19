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
@st.cache_data
def load_data():
    data1,data2,data3=getData()
    
    
    
    return data1,data2,data3 

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

sport_events= st.multiselect("Choisir un évenement", 
                             data2["year"].sort_values().unique(), 
                             placeholder=None,
                             label_visibility="visible", 
                             accept_new_options=False, 
                             width="stretch")

fede_filter= st.multiselect("Choisir une/des fédération/s", 
                             data1["nom_fed"].sort_values().unique(), 
                             placeholder=None,
                             label_visibility="visible", 
                             accept_new_options=False, 
                             width="stretch")


if len(sport_events)>0:
    event_coverage= data2[data2["sport_event"].isin(sport_events)]
else:
    event_coverage=data2

if len(fede_filter)>0:
    license_filters= data1[data1["nom_fed"].isin(fede_filter)]
else:
    license_filters=data1
    
fig_media_lic=stg.graph_comparaison_media_lic(license_filters,event_coverage,data3,sport_events)
# APPELER LA FONCTION PERMETTANT LA GEN DU GRAPH EN DESSOUS ####
# NOM_VARIABLE_FILTRE= st.multiselect("CHOISIR LE TITRE DU FILTRE", 
#                               DATA_A_FILTRER["FILTRE"].sort_values().unique(), 
#                               placeholder=None,
#                               label_visibility="visible", 
#                               accept_new_options=False, 
#                               width="stretch")

# RAJOUTER LA FONCTION SOUS LA FORME 
# NOM_GRAPH = stg.NOM_DE_LA_FONCTION(VOS_VARIABLES)

st.plotly_chart(fig_media_lic, use_container_width='stretch')
# AJOUTER st.plotly_chart( VOTRE_GRAPH, use_container_width='stretch') en dessous


