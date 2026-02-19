import streamlit as st
import pandas as pd
import plotly.express as px
import app as mn
from utils import sidebar_filters, apply_filters

df = mn.data1
f = sidebar_filters(df)
dff = apply_filters(df, f)

st.title("Analyse par tranches d'âge")

# controls
col1, col2, col3 = st.columns([2, 2, 3])

with col1:
    années = sorted(dff["year"].unique())
    année_choisie = st.selectbox("Année", années)

with col2:
    mode = st.radio("Affichage", ["Volumes", "% du total"], horizontal=True)

with col3:
    barmode = st.radio("Mode graphique", ["Groupé", "Empilé", "Pyramide"], horizontal=True)

dff_year = dff[dff["year"] == année_choisie]

# data
colonnes_age_h = ["h_1_9", "h_10_19", "h_20_29", "h_30_59", "h_60_74", "h_75"]
colonnes_age_f = ["f_1_9", "f_10_19", "f_20_29", "f_30_59", "f_60_74", "f_75"]
labels = ["1-9", "10-19", "20-29", "30-59", "60-74", "75+"]

tot_h = dff_year[colonnes_age_h].sum().values
tot_f = dff_year[colonnes_age_f].sum().values

age = pd.DataFrame({"Tranche": labels, "Hommes": tot_h, "Femmes": tot_f})
age["Total"] = age["Hommes"] + age["Femmes"]

total_general   = age["Total"].sum()
total_h_global  = age["Hommes"].sum()
total_f_global  = age["Femmes"].sum()
tranche_dominante = age.loc[age["Total"].idxmax(), "Tranche"]

# kpi info
k1, k2, k3, k4 = st.columns(4)
k1.metric(" Population licenciés", f"{total_general:,.0f}")
k2.metric(" Total Hommes",      f"{total_h_global:,.0f}")
k3.metric(" Total Femmes",      f"{total_f_global:,.0f}")


st.divider()

# disposition
col_bar, col_donut = st.columns([3, 2])

# hist
plot_df = age.melt(id_vars=["Tranche"], value_vars=["Hommes", "Femmes"],
                   var_name="Sexe", value_name="Valeur")

if mode == "% du total":
    total_val = plot_df["Valeur"].sum()
    plot_df["Valeur"] = (plot_df["Valeur"] / total_val * 100).round(2)

with col_bar:
    if barmode == "Pyramide":
        import plotly.graph_objects as go
        x_h = -age["Hommes"] if mode == "Volumes" else -(age["Hommes"] / total_general * 100)
        x_f =  age["Femmes"] if mode == "Volumes" else  (age["Femmes"] / total_general * 100)

        fig = go.Figure()
        fig.add_trace(go.Bar(y=labels, x=x_h, name="Hommes", orientation="h"))
        fig.add_trace(go.Bar(y=labels, x=x_f, name="Femmes", orientation="h"))
        fig.update_layout(barmode="overlay",
                          title=f"Pyramide des âges — {année_choisie}")
    else:
        bm = "group" if barmode == "Groupé" else "stack"
        fig = px.bar(plot_df, x="Tranche", y="Valeur", color="Sexe",
                     barmode=bm, text_auto=".2s",
                     title=f"Répartition par tranche d'âge — {année_choisie}",
                     labels={"Valeur": "%" if mode == "% du total" else "Valeur"})

    st.plotly_chart(fig, use_container_width=True)

# pie chart
with col_donut:
    fig_donut = px.pie(
        names=["Hommes", "Femmes"],
        values=[total_h_global, total_f_global],
        hole=0.55,
        title="Part H / F globale",
    )
    st.plotly_chart(fig_donut, use_container_width=True)
