import streamlit as st
import pandas as pd
import numpy as np
from utils import sidebar_filters, apply_filters
import streamlit_app as mn
import plotly.express as px
import json

st.set_page_config(
    page_title="Vue d'ensemble du sport en France",
    page_icon="💪",
    layout="wide"
)
with st.sidebar:
    st.page_link("streamlit_app.py", label="Accueil", icon="🏠")
    st.page_link("pages/1_Vue_ensemble.py", label="Vue d'ensemble du sport en France", icon="💪")
    st.page_link("pages/2_Analyse_temporelle.py", label="Analyse temporelle du sport en France", icon="📈")
    st.page_link("pages/3_Analyse_sexe.py", label="Sport & Femmes : Les médias comme levier ?", icon="♀️")
    st.page_link("pages/4_Annexes.py", label="Annexes ", icon="📋")
df = mn.data1
data4=pd.read_csv("pop_by_region.csv")
f = sidebar_filters(df)
dff = apply_filters(df, f)

st.title("📊 Vue d’ensemble")


if "page" not in st.session_state:
    st.session_state.page = "Accueil"

flex = st.container(horizontal=True, horizontal_alignment="right")

buttons = ["Overview du sport en France", "Médiatisation du sport", "Représentation des femmes"]

for name in buttons:
    if flex.button(name):
        st.session_state.page = name




# container = st.container(border=True)

# with container:
#     st.header("Insights")
#     st.write("- 48,1% de licenciés entre 2012 et 2023 : 11,2m à 16,5m")
#     st.write("- 2021 : un drop qui s'explique par la période du COVID. Rattrapé ensuite en 2022")
#     st.write(" - un insight sur la répartition des licenciés en FR")
#     st.write("- un insight sur l'évolution des fédérations en FR")


st.markdown("""
<style>
.custom-box {
    max-width: 1500px;
    margin-left: auto;
    margin-right: auto;
    border: 6px solid indianred;
    padding: 50px;
    border-radius: 5px;
    box-shadow: 2px 4px 12px rgba(0,0,0,0.15);
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="custom-box">
    <h4>Insights</h4>
    <h2>La pratique du sport au sein des fédérations, en augmentation depuis 2012</h2>
    <ul>
        <li><b>48,1%</b> de licenciés entre 2012 et 2023 : : 11,2m à 16,5m</li>
        <li><b>2021</b> : un drop qui s'explique par la période du COVID. Rattrapé ensuite en 2022</li>
        <li>Au total fédérations, <b>l'Île de France</b> est la région qui présente le plus de licenciés (15,5% du total)</li>
        <li><b>Guyane, Martinique, Guadeloupe, Réunion & Corse</b> : une progression insulaire marquée sur la période</li>
        <li><b>Les 20-29 ans</b> : la tranche d'âge en décrochage après les +75ans. Ils représentaient 9,6% du total en 2023.</li>
        <li>Les fédérations qui ont le plus augmenté au cours de la période sont la <b>fédération de Football</b> (+381k), <b>d'Union Scolaire</b> (+310k), <b>du Basketball</b> (+121k), <b>de Tir</b> (+111k) et <b>de natation</b> (+107k) </li>
    </ul>

</div>
""", unsafe_allow_html=True)

st.header(" ")
st.subheader("Aperçu des données")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Période", f"{dff['year'].min()} → {dff['year'].max()}")
c2.metric("Observations", f"{len(dff):,}".replace(",", " "))
c3.metric("Régions", dff["region"].nunique())
c4.metric("Fédérations", dff["nom_fed"].nunique())


st.dataframe(dff.head(50), use_container_width=True)

st.divider()

st.subheader("Analyse par région")
### CARTE DE FRANCEE
c1, c2 = st.columns(2)


with c1:
    year_select= st.selectbox("Choisir une année", 
                             df["year"].sort_values().unique(), 
                             placeholder=None,
                             label_visibility="visible", 
                             accept_new_options=False, 
                             width="stretch")
    if len(str(year_select))>0:
        dftemp=df[df["year"]==year_select]
    else:
        dftemp=df[df["year"]==2012]
    with open("regions.geojson", "r", encoding="utf-8") as regjson:
        regions_geojson = json.load(regjson)

        
        dftemp["region"]=dftemp["region"].replace({"dAzur":"d'Azur"}, regex=True)
        print(dftemp["region"].unique())
        df_region = dftemp.groupby(["year","region"], as_index=False).agg(total_lic=(
            "total_lic", "sum"), total_f=(
            "total_f", "sum"),total_h=(
            "total_h", "sum"
            ))


    df_region = df_region.merge(data4, left_on="region", right_on="reg", how="left")

    df_region["ratio_licencié_habitant"] = df_region["total_lic"] / df_region["pop"]
    df_region["ratio_f"] = df_region["total_f"] / df_region["pop"]



    st.subheader(f"Ratio licenciés / habitant par région - {year_select}")

    fig_map = px.choropleth(
        df_region,
        geojson=regions_geojson,
        locations="region",
        featureidkey="properties.nom",  
        color="ratio_licencié_habitant",
        hover_name="region",
        color_continuous_scale="Viridis",
        range_color=[0, 0.3]
        
    )

    fig_map.update_geos(fitbounds="locations", visible=False)
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    st.plotly_chart(fig_map, use_container_width=True)

with c2:

    f_for_rank = dict(f)
    f_for_rank["region"] = "Toutes"

    dff = apply_filters(df, f_for_rank)



    metric = st.selectbox("Indicateur", ["total_lic", "total_h", "total_f"])
    top_n = st.slider("Top N régions", 5, 30, 18)

    by_region = dff.groupby("region")[metric].sum().sort_values(ascending=False)
    total_nat = by_region.sum()

    rank = by_region.reset_index().rename(columns={metric: "Total"})
    rank["Part (%)"] = (rank["Total"] / total_nat * 100).round(2)

    st.dataframe(rank, use_container_width=True)

st.divider()



#### Separation age 
st.subheader("Comparaison par tranche d'âge et sexe")
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


st.divider()

st.subheader("Analyse par fédération")
# controle
col1, col2, col3 = st.columns(3)

with col1:
    années = sorted(dff["year"].unique())
    année_choisie = st.selectbox(" Année", années)

with col2:
    metric = st.selectbox(" Indicateur", {
        "total_lic": "Total licenciés",
        "total_h":   "Hommes",
        "total_f":   "Femmes",
    }.keys(), format_func=lambda x: {
        "total_lic": "Total licenciés",
        "total_h":   "Hommes",
        "total_f":   "Femmes",
    }[x])

with col3:
    top_n = st.slider(" Top N fédérations", 5, 50, 15)

dff_year = dff[dff["year"] == année_choisie]

# calculs
by_fed = dff_year.groupby("nom_fed")[metric].sum().sort_values(ascending=False)
total_global = by_fed.sum()
top3_share= by_fed.head(3).sum() / total_global * 100 if total_global else 0
top1_fed = by_fed.index[0] if len(by_fed) > 0 else "—"
nb_feds = len(by_fed)

# kpi
k1, k2, k3, k4 = st.columns(4)
k1.metric(" Total licenciés", f"{total_global:,.0f}")
k2.metric(" N°1", top1_fed)
k3.metric(" Part du Top 3", f"{top3_share:.1f}%")


c1, c2 = st.columns(2)


# graph
table = by_fed.reset_index().rename(columns={metric: "Total"})
with c1:
    fig = px.bar(
        table.head(top_n).sort_values("Total"),
        x="Total", y="nom_fed", orientation="h",
        title=f"Top {top_n} fédérations — {année_choisie}",
        labels={"nom_fed": "Fédération", "Total": "Licenciés"},
        text_auto=".2s",
    )
    fig.update_layout(yaxis_title="", xaxis_title="Licenciés")
    st.plotly_chart(fig, use_container_width=True)

# tableau
with c2:

    table["% du total"] = (table["Total"] / total_global * 100).round(1).astype(str) + "%"
    st.dataframe(table, use_container_width=True, hide_index=True)

st.divider()
#### ptit points qui dance


df_grouped = df.groupby(['nom_fed','year'], as_index=False)['total_lic'].sum()

df_grouped = df_grouped.sort_values(['nom_fed','year'])

df_grouped['progression_pct'] = (
    df_grouped.groupby('nom_fed')['total_lic']
              .pct_change() 
              *100
)


fig = px.scatter(
    df_grouped,
    x="total_lic",
    y="progression_pct",
    animation_frame="year",
    animation_group="nom_fed",
    hover_name="nom_fed",
    labels={
        "total lics": "Total licenciés",
        "progression_pct": "Progression depuis l'origine",
        "year": "Année"
    },
    title="Évolution des licenciés par fédération",
    height=750
)

fig.add_vline(x=50, line_dash="dash", line_color="red", opacity=0.5)
fig.add_hline(y=0, line_dash="dash", line_color="red", opacity=0.5)

fig.update_xaxes(range=[df_grouped["total_lic"].min(), df_grouped["total_lic"].max()])
fig.update_yaxes(range=[-35,35])

st.plotly_chart(fig, use_container_width=True)