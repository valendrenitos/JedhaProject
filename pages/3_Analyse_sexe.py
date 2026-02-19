import streamlit as st
import pandas as pd
import plotly.express as px
import app as mn
from utils import sidebar_filters, apply_filters
import streamlit_graphs as stg
df = mn.data1
data2=mn.data2
f = sidebar_filters(df)
dff = apply_filters(df, f)

st.title("🚻 Analyse Hommes / Femmes")



######~INSIGHT MEDIA


sex = dff.groupby("year")[["total_h", "total_f"]].sum().reset_index()
sex["total"] = sex["total_h"] + sex["total_f"]
sex["part_h"] = sex["total_h"] / sex["total"] * 100
sex["part_f"] = sex["total_f"] / sex["total"] * 100

c1, c2, c3 = st.columns(3)
c1.metric("Moyenne hommes (%)", f"{sex['part_h'].mean():.1f}")
c2.metric("Moyenne femmes (%)", f"{sex['part_f'].mean():.1f}")
c3.metric("Total période", f"{sex['total'].sum():,.0f}".replace(",", " "))

mode = st.radio("Affichage", ["Volumes", "Parts (%)"], horizontal=True)

if mode == "Volumes":
    fig = px.line(sex, x="year", y=["total_h", "total_f"], markers=True,
                  title="Évolution des licences par sexe")
else:
    fig = px.line(sex, x="year", y=["part_h", "part_f"], markers=True,
                  title="Parts (%) par sexe")

st.plotly_chart(fig, use_container_width=True)
st.dataframe(sex, use_container_width=True)











datatreated1=df.groupby(["year"], as_index=False).agg(total_f=('total_f','sum'))   
data2=data2[data2['genre']=='féminin']
fig_media_lic=stg.graph_comparaison_media_lic_sex(datatreated1,data2)


st.plotly_chart(fig_media_lic, use_container_width='stretch')