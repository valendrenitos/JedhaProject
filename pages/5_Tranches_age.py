import streamlit as st
import pandas as pd
import plotly.express as px
import app as mn
from utils import sidebar_filters, apply_filters

df = mn.data1
f = sidebar_filters(df)
dff = apply_filters(df, f)

st.title("🎂 Analyse par tranches d’âge")

colonnes_age_h = ["h_1_9", "h_10_19", "h_20_29", "h_30_59", "h_60_74", "h_75"]
colonnes_age_f = ["f_1_9", "f_10_19", "f_20_29", "f_30_59", "f_60_74", "f_75"]
labels = ["1-9", "10-19", "20-29", "30-59", "60-74", "75+"]

tot_h = dff[colonnes_age_h].sum().values
tot_f = dff[colonnes_age_f].sum().values

age = pd.DataFrame({"Tranche": labels, "Hommes": tot_h, "Femmes": tot_f})
age["Total"] = age["Hommes"] + age["Femmes"]

mode = st.radio("Affichage", ["Volumes", "% du total"], horizontal=True)

plot_df = age.melt(id_vars=["Tranche"], value_vars=["Hommes", "Femmes"], var_name="Sexe", value_name="Valeur")

if mode == "% du total":
    total = plot_df["Valeur"].sum()
    plot_df["Valeur"] = plot_df["Valeur"] / total * 100

fig = px.bar(plot_df, x="Tranche", y="Valeur", color="Sexe", barmode="group",
             title="Répartition par tranche d’âge")
st.plotly_chart(fig, use_container_width=True)

st.dataframe(age, use_container_width=True)
