import pandas as pd
import streamlit as st 
import plotly.express as px 
import plotly.graph_objects as go
import numpy as np

from DBConnector import getData


st.set_page_config(
    page_title="Projet Final jedha DAFS-16",
    page_icon="💸 ",
    layout="wide"
)
@st.cache_data
def load_data():
    data1,data2=getData()
    return data1,data2 

data1,data2=load_data()

st.subheader("Problématique")

st.markdown("""
    Mettre la problématique ici
""")

st.markdown("Selection du sport")


feds = st.selectbox("federation", data1["federation"].sort_values().unique())
    

evenement = data2[data2["sport"] == feds]


fig = px.histogram(evenement, x="Date", y="telespectateur")
fig.update_layout(bargap=0.2)


st.plotly_chart(fig, use_container_width=True)
data_load_state = st.text('Loading data...')

