import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit_app as mn
from utils import sidebar_filters, apply_filters
import streamlit_graphs as stg
from scipy.interpolate import Akima1DInterpolator
import ML_function as mlf
import numpy as np
df = mn.data1
with st.sidebar:
    st.page_link("streamlit_app.py", label="Accueil", icon="🏠")
    st.page_link("pages/1_Vue_ensemble.py", label="Vue d'ensemble du sport en France", icon="💪")
    st.page_link("pages/2_Analyse_temporelle.py", label="Analyse temporelle du sport en France", icon="📈")
    st.page_link("pages/3_Analyse_sexe.py", label="Sport & Femmes : Les médias comme levier ?", icon="♀️")
    st.page_link("pages/4_Annexes.py", label="Annexes ", icon="📋")
f = sidebar_filters(df)
dff = apply_filters(df, f)
st.set_page_config(
    page_title="Analyse temporelle du sport en France",
    page_icon="📈",
    layout="wide"
)


data1=mn.data1
data3=mn.data3
data2=mn.data2



st.title("La médiatisation du sport, vecteur d'augmentation des licences sportives")

st.markdown("""
<style>
.custom-box {
    max-width: 1500px;
    margin-left: auto;
    margin-right: auto;
    border: 6px solid indianred;
    padding: 20px;
    border-radius: 5px;
    box-shadow: 2px 4px 12px rgba(0,0,0,0.15);
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="custom-box">
    <h4>Insights</h4>
    <h2>Une augmentation des audiences TV continue sur la période</h2>
    <ul>
        <li>Un effet JO marqué : un nombre de licences à la hausse après des événements sportifs très médiatisés</li>
        <li>Une tendance à la hausse qui vient confirmer des prédictions d'augmentation du nombre de licences </li>
        <li>Des événements sportifs masculins qui demeurent les plus médiatisés à la TV</li>
        <li>Un effet COVID qui a redonné de l'élan à la médiatisation du sport</li>
    </ul>

</div>
""", unsafe_allow_html=True)
st.divider()

st.subheader("Analyse du nombre de licenciés sur les années")
metrics_list = [
    ("Licenciés total", "total_lic"),
    ("Hommes",          "total_h"),
    ("Femmes",          "total_f"),
]
display_name, metric = st.selectbox(
    "Indicateur",
    options=metrics_list,
    format_func=lambda x: x[0]             
)
ts = dff.groupby("year")[metric].sum().reset_index()
ts["variation_%"] = ts[metric].pct_change() * 100



c1, c2 = st.columns(2)
with c1:
    st.dataframe(ts, use_container_width=True)

with c2:
    mode = st.radio("Affichage", ["Niveau", "Variation (%)"], horizontal=True)
    if mode == "Niveau":
        fig = px.line(ts, x="year", y=metric, markers=True, title=f"Évolution — {display_name}")
    else:
        fig = px.bar(ts, x="year", y="variation_%", title=f"Variation annuelle (%) — {display_name}")
    st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("Comparaison des pics de médias sportif et du nombre de licenciés")
sport_events= st.multiselect("Choisir une année", 
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
 
datatreated1=data1.groupby(["year"], as_index=False).agg(total_lic=('total_lic','sum'))   

fig_media_lic=stg.graph_comparaison_media_lic(datatreated1,event_coverage,data3,sport_events)


st.plotly_chart(fig_media_lic, use_container_width='stretch')
st.divider()
st.subheader("Comparaison entre les sports féminins et masculins dans les médias")
######## CAMEMBERT
year_filter2= st.selectbox("Choisir une année", 
                             data2["year"].sort_values().unique(), 
                             placeholder=None,
                             label_visibility="visible", 
                             accept_new_options=False, 
                             width="stretch")
if len(str(year_filter2))>0:
    year_filters= data2[data2["year"]==year_filter2]
else:
    year_filters=data2


fig_target=stg.pie_chart(year_filters)
st.plotly_chart(fig_target, use_container_width=True)

st.divider()
st.subheader("Prévision de l'évolution du nombre de licences")

fed = st.selectbox("Choississez une fédération", 
                   data1["nom_fed"].sort_values().unique())
year = st.selectbox("Choississez une année",
                   np.arange(2024,2041))



df_filtered=data1[data1["nom_fed"]==fed]
try:
    df_future_pred = mlf.LinReg(df_filtered, year)

    x=df_future_pred["year"]
    y=df_future_pred["total_lic"]

    xs = np.linspace(min(x), max(y),num=100)
    y_akima = Akima1DInterpolator(x, y, method="akima")(xs)

    #st.line_chart(xs, x="x")
    fig = px.line(df_future_pred, x="year", y="total_lic", title='pred')
    st.plotly_chart(fig, use_container_width=True)
except:
    st.write("Data insuffisante pour "+fed)

