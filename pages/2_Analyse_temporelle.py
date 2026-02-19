import streamlit as st
import pandas as pd
import plotly.express as px
import app as mn
from utils import sidebar_filters, apply_filters
import streamlit_graphs as stg
from scipy.interpolate import Akima1DInterpolator
import ML_function as mlf
import numpy as np
df = mn.data1
f = sidebar_filters(df)
dff = apply_filters(df, f)

st.title("📈 Analyse temporelle")

data1=mn.data1
data3=mn.data3
data2=mn.data2


metric = st.selectbox("Indicateur", ["total_lic", "total_h", "total_f"])
ts = dff.groupby("year")[metric].sum().reset_index()
ts["variation_%"] = ts[metric].pct_change() * 100

c1, c2 = st.columns(2)
with c1:
    st.dataframe(ts, use_container_width=True)

with c2:
    mode = st.radio("Affichage", ["Niveau", "Variation (%)"], horizontal=True)
    if mode == "Niveau":
        fig = px.line(ts, x="year", y=metric, markers=True, title=f"Évolution — {metric}")
    else:
        fig = px.bar(ts, x="year", y="variation_%", title=f"Variation annuelle (%) — {metric}")
    st.plotly_chart(fig, use_container_width=True)

data3.loc[(data3["annee"] >= 2016) & (data3["annee"] <= 2024), "total"] /= 2.6
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
 
datatreated1=data1.groupby(["year"], as_index=False).agg(total_license=('total_lic','sum'))   
fig_media_lic=stg.graph_comparaison_media_lic(datatreated1,event_coverage,data3,sport_events)


st.plotly_chart(fig_media_lic, use_container_width='stretch')


######## CAMEMBERT





fed = st.selectbox("Select a fed you want to see preds", 
                   data1["nom_fed"].sort_values().unique())
year = st.selectbox("Select a year you want to see your pred",
                   np.arange(2024,2041))



df_filtered=data1[data1["nom_fed"]==fed]
try:
    df_future_pred = mlf.LinReg(df_filtered, year)

    

    st.write(f"Prediction for {year}:",year)
    st.write("Future predictions:")
    st.dataframe(df_future_pred)



    x=df_future_pred["year"]
    y=df_future_pred["total_lic"]

    xs = np.linspace(min(x), max(y),num=100)
    y_akima = Akima1DInterpolator(x, y, method="akima")(xs)

    #st.line_chart(xs, x="x")
    fig = px.line(df_future_pred, x="year", y="total_lic", title='pred')
    st.plotly_chart(fig, use_container_width=True)
except:
    st.write("Data insuffisante pour "+fed)

