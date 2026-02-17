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

data1,data2,data3=load_data()



# DATA 1 : LICENSES : COLONNES : year,  region,  nom_fed, total_lic, total_f, total_h, h_1_9, h_10_19, h_20_29,h_30_59,h_60_74, h_75, f_1_9, f_10_19, f_20_29, f_30_59, f_60_74, f_75
# DATA 2 : Medias : sport_event,sport,year,avrg_tv_aud,avrg_tv_match,total_match,hours_live,numb_of_post
# DATA 3 Club 49-23 : annee,  olympics,  non_olympics, affinitaire, scholair, total

st.subheader("Problématique")

st.markdown("""
    Mettre la problématique ici
""")

sport_events= st.multiselect("Select sportive events", 
                             data2["year"].sort_values().unique(), 
                             placeholder=None,
                             label_visibility="visible", 
                             accept_new_options=False, 
                             width="stretch")

if len(sport_events)>0:
    event_coverage= data2[data2["sport_event"].isin(sport_events)]
else:
    event_coverage=data2

fig_media_lic=stg.graph_comparaison_media_lic(data1,data2,data3,sport_events)
# fig = px.line(x=datatreated1["year"], y=datatreated1["total_license"], color=px.Constant("This year"),
#              labels=dict(x="année", y="licenses", color="Time Period"))
# fig.add_bar(event_coverage, 
#                  x = "annee", 
#                  y="avrg_tv_aud",
#                  name= "Average TV coverage for selected events" if len(sport_events)>0 else "Average TV coverage for all events",
#                  color="sport")
# fig.update_layout(bargap=0.2)

st.plotly_chart(fig_media_lic, use_container_width='stretch')



