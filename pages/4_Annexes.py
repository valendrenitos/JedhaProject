import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit_app as mn
from utils import sidebar_filters, apply_filters
with st.sidebar:
   
    st.page_link("pages/1_Vue_ensemble.py", label="Vue d'ensemble du sport en France", icon="💪")
    st.page_link("pages/2_Analyse_temporelle.py", label="Analyse temporelle du sport en France", icon="📈")
    st.page_link("pages/3_Analyse_sexe.py", label="Sport & Femmes : Les médias comme levier ?", icon="♀️")
    st.page_link("pages/4_Annexes.py", label="Annexes ", icon="📋")
df = mn.data1
f = sidebar_filters(df)
dff = apply_filters(df, f)

st.title("Analyse par fédération")

# Sélecteur d'année
années = sorted(dff["year"].unique())
année_choisie = st.selectbox("Année", années)
dff = dff[dff["year"] == année_choisie]

metric = st.selectbox("Indicateur", ["total_lic", "total_h", "total_f"])
top_n = st.slider("Top N", 5, 50, 15)

by_fed = dff.groupby("nom_fed")[metric].sum().sort_values(ascending=False)
total_global = by_fed.sum()
top3_share = (by_fed.head(3).sum() / total_global * 100) if total_global else 0

st.metric("Part du Top 3 (%)", f"{top3_share:.1f}")

table = by_fed.reset_index().rename(columns={metric: "total"})
st.dataframe(table.head(50), use_container_width=True)

fig = px.bar(
    table.head(top_n).sort_values("total"),
    x="total", y="nom_fed", orientation="h",
    title=f"Top {top_n} fédérations – {metric}"
)
st.plotly_chart(fig, use_container_width=True)

f_for_rank = dict(f)
f_for_rank["region"] = "Toutes"

dff = apply_filters(df, f_for_rank)

st.title(" Analyse régions")


by_region = dff.groupby("region")[metric].sum().sort_values(ascending=False)
total_nat = by_region.sum()

rank = by_region.reset_index().rename(columns={metric: "Total"})
rank["Part (%)"] = (rank["Total"] / total_nat * 100).round(2)

st.dataframe(rank, use_container_width=True)

fig_histo = px.bar(rank.head(top_n).sort_values("Total"), x="Total", y="region", orientation="h",
             title=f"Top {top_n} régions — {metric}")
st.plotly_chart(fig_histo, use_container_width=True)



st.title("Analyse par tranches d'âge")

# controls
col1, col2, col3 = st.columns([2, 2, 3])

with col1:
    années = sorted(dff["year"].unique())
   

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


st.title(" Parité dans les fédérations sportives")
st.divider()

# controleurs

min_total = st.slider("Seuil minimal de licences", 0, 200000, 10000, step=1000)

dff_year = dff[dff["year"] == année_choisie]

# calcules
parite = dff_year.groupby("nom_fed", as_index=False).agg(
    total_lic=("total_lic", "sum"),
    total_f=("total_f", "sum"),
    total_h=("total_h", "sum"),
)
parite["part_femmes"] = (parite["total_f"] / parite["total_lic"] * 100).round(1)
parite = parite[parite["total_lic"] >= min_total].sort_values("part_femmes", ascending=False)

# kpi
nb_paritaires = ((parite["part_femmes"] >= 45) & (parite["part_femmes"] <= 55)).sum()
part_moy = parite["part_femmes"].mean()
plus_fem  = parite.iloc[0]["nom_fed"]  if len(parite) > 0 else "—"
moins_fem = parite.iloc[-1]["nom_fed"] if len(parite) > 0 else "—"

k1, k2, k3, k4 = st.columns(4)
k1.metric(" Fédérations analysées", len(parite))
k2.metric(" Part femmes moyenne", f"{part_moy:.1f}%")
k3.metric(" Plus féminisée",plus_fem)
k4.metric(" Moins féminisée", moins_fem)

st.divider()

# Top 10 plus / moins féminisées
cols = ["nom_fed", "part_femmes", "total_lic"]
col_labels = {"nom_fed": "Fédération", "part_femmes": "% Femmes", "total_lic": "Licences"}

c1, c2 = st.columns(2)
with c1:
    st.subheader(" Top 10 — plus féminisées")
    st.dataframe(
        parite.head(10)[cols].rename(columns=col_labels),
        use_container_width=True, hide_index=True,
    )
with c2:
    st.subheader(" Top 10 — moins féminisées")
    st.dataframe(
        parite.tail(10).sort_values("part_femmes")[cols].rename(columns=col_labels),
        use_container_width=True, hide_index=True,
    )

st.divider()

# histo
st.subheader("Distribution de la part des femmes")

fig = px.histogram(
    parite, x="part_femmes", nbins=30,
    title=f"Répartition des fédérations par part des femmes — {année_choisie}",
    labels={"part_femmes": "Part des femmes (%)"},
)
fig.add_vline(x=50, line_dash="dash", annotation_text="Parité (50%)", annotation_position="top right")
fig.add_vline(x=part_moy, line_dash="dot", annotation_text=f"Moyenne ({part_moy:.1f}%)", annotation_position="top left")
fig.update_layout(bargap=0.1, xaxis_range=[0, 100])
st.plotly_chart(fig, use_container_width=True)

# splatter
st.subheader("Taille vs féminisation")

fig2 = px.scatter(
    parite, x="total_lic", y="part_femmes",
    hover_name="nom_fed",
    labels={"total_lic": "Nombre de licences", "part_femmes": "Part des femmes (%)"},
    title="Nombre de licences vs part des femmes",
    size="total_lic", size_max=40,
)
fig2.add_hline(y=50, line_dash="dash", annotation_text="Parité")
st.plotly_chart(fig2, use_container_width=True)


st.title(" Parité dans les fédérations")

min_total = st.slider("Seuil minimal de licences sur la période", 0, 200000, 10000, step=1000)

parite = dff.groupby(["year","nom_fed"], as_index=False).agg(total_license=("total_lic","sum"),
                                   total_f=("total_f","sum"),
                                   total_h=("total_h","sum"))
parite["part_femmes"] = parite["total_f"] / parite["total_license"] * 100
parite = parite[parite["total_license"] > min_total].sort_values("part_femmes", ascending=False)

c1, c2 = st.columns(2)
with c1:
    st.subheader("Top 10 — les plus féminisées")
    st.dataframe(parite.head(10)[["nom_fed","part_femmes","total_license"]], use_container_width=True)
with c2:
    st.subheader("Top 10 — les moins féminisées")
    st.dataframe(parite.tail(10)[["nom_fed","part_femmes","total_license"]].sort_values("part_femmes"),
                 use_container_width=True)

fig = px.histogram(parite, x="part_femmes", nbins=30, title="Distribution de la part des femmes (%)")
fig.update_layout(bargap=0.2)    
st.plotly_chart(fig, use_container_width=True)


st.title(" Féminisation des fédérations sportives")

# anneés 
années_dispo = sorted(dff["year"].unique())
année_debut  = années_dispo[0]
année_fin    = années_dispo[-1]

st.caption(f"Analyse de l'évolution de la part des femmes — {année_debut} → {année_fin}")
st.divider()

# agg anne fed
evol = dff.groupby(["nom_fed", "year"], as_index=False).agg(
    total_lic=("total_lic", "sum"),
    total_f=("total_f", "sum"),
)
evol["part_femmes"] = evol["total_f"] / evol["total_lic"] * 100

# 2012 - 2023
p_debut = (
    evol[evol["year"] == année_debut][["nom_fed", "part_femmes"]]
    .rename(columns={"part_femmes": f"part_{année_debut}"})
)
p_fin = (
    evol[evol["year"] == année_fin][["nom_fed", "part_femmes"]]
    .rename(columns={"part_femmes":f"part_{année_fin}"})
)

evo = p_debut.merge(p_fin, on="nom_fed", how="inner")
evo["variation (pts)"] = evo[f"part_{année_fin}"] - evo[f"part_{année_debut}"]

# Licences fin de période
lic_fin = (
    dff[dff["year"] == année_fin]
    .groupby("nom_fed", as_index=False)["total_lic"]
    .sum()
    .rename(columns={"total_lic": f"licences_{année_fin}"})
)
evo = evo.merge(lic_fin, on="nom_fed", how="left")
evo = evo.sort_values("variation (pts)", ascending=False)

# kpi
part_globale_debut = (
    dff[dff["year"] == année_debut]["total_f"].sum()
    / dff[dff["year"] == année_debut]["total_lic"].sum() * 100
)
part_globale_fin = (
    dff[dff["year"] == année_fin]["total_f"].sum()
    / dff[dff["year"] == année_fin]["total_lic"].sum() * 100
)
top_progresseur  = evo.iloc[0]["nom_fed"] if len(evo) > 0 else "—"
top_regresseur   = evo.iloc[-1]["nom_fed"] if len(evo) > 0 else "—"

k1, k2, k3, k4 = st.columns(4)
k1.metric(f"♀️ Part femmes {année_debut}", f"{part_globale_debut:.1f}%")
k2.metric(f"♀️ Part femmes {année_fin}",   f"{part_globale_fin:.1f}%")

st.divider()

# Tableau
col_ctrl1, col_ctrl2 = st.columns([2, 3])
with col_ctrl1:
    top_n = st.slider("Top N fédérations", 5, 50, 20)
with col_ctrl2:
    sens = st.radio("Trier par", ["Plus grande progression", "Plus grande régression"],
                    horizontal=True)

evo_sorted = evo if sens == "Plus grande progression" else evo.sort_values("variation (pts)")

st.subheader(f"Top {top_n} — {sens} ({année_debut} → {année_fin})")

evo_display = evo_sorted.head(top_n).copy()
for col in [f"part_{année_debut}", f"part_{année_fin}", "variation (pts)"]:
    evo_display[col] = evo_display[col].round(1)

st.dataframe(evo_display, use_container_width=True, hide_index=True)

st.divider()

# graph
st.subheader(f"Variation de la part des femmes par fédération ({année_debut} → {année_fin})")

fig_bar = px.bar(
    evo_sorted.head(top_n).sort_values("variation (pts)"),
    x="variation (pts)", y="nom_fed", orientation="h",
    text_auto=".1f",
    labels={"nom_fed": "Fédération"},
    color="variation (pts)",
    color_continuous_scale="RdYlGn",
    color_continuous_midpoint=0,
)
fig_bar.update_layout(
    yaxis_title="",
    xaxis_title="Variation (points de %)",
    coloraxis_showscale=False,
)
st.plotly_chart(fig_bar, use_container_width=True)

st.divider()

# courbe par federation
st.subheader("Évolution annuelle par fédération")

col_fed, col_ref = st.columns([3, 2])
with col_fed:
    fed = st.selectbox("Choisir une fédération", sorted(evol["nom_fed"].unique()))
with col_ref:
    show_moyenne = st.toggle("Afficher la moyenne générale", value=True)

curve = evol[evol["nom_fed"] == fed].sort_values("year")

fig_line = px.line(
    curve, x="year", y="part_femmes",
    markers=True,
    title=f"Part des femmes — {fed}",
    labels={"year": "Année", "part_femmes": "Part des femmes (%)"},
)

if show_moyenne:
    moyenne_annuelle = evol.groupby("year")["part_femmes"].mean().reset_index()
    fig_line.add_scatter(
        x=moyenne_annuelle["year"],
        y=moyenne_annuelle["part_femmes"],
        mode="lines",
        name="Moyenne toutes fédérations",
        line=dict(dash="dash"),
    )

fig_line.update_layout(
    xaxis_title="Année",
    yaxis_title="Part des femmes (%)",
    yaxis=dict(range=[0, 100]),
)
st.plotly_chart(fig_line, use_container_width=True)

# agg / année
evol = dff.groupby(["nom_fed", "year"], as_index=False).agg(
    total_license=("total_lic", "sum"),
    total_f=("total_f", "sum")
)

evol["part_femmes"] = evol["total_f"] / evol["total_license"] * 100

# Parts en 2012 et 2022
p2012 = evol[evol["year"] == 2012][["nom_fed", "part_femmes"]].rename(
    columns={"part_femmes": "part_femmes_2012"}
)
p2023 = evol[evol["year"] == 2023][["nom_fed", "part_femmes"]].rename(
    columns={"part_femmes": "part_femmes_2023"}
)

evo = p2012.merge(p2023, on="nom_fed", how="inner")

# variation en points de %
evo["variation_absolue"] = evo["part_femmes_2023"] - evo["part_femmes_2012"]


lic_2023 = (
    dff[dff["year"] == 2023]
    .groupby("nom_fed", as_index=False)["total_lic"]
    .sum()
    .rename(columns={"total_lic": "licences_2023"})
)

evo = evo.merge(lic_2023, on="nom_fed", how="left")


# evolution feminisation
evo = evo.sort_values("variation_absolue", ascending=False)

# tableau top
top_n = st.slider("Top N", 5, 50, 20)
st.subheader(f"Top {top_n} fédérations — progression de la part des femmes (2012 - 2023)")

# (arrondi)
evo_display = evo.copy()
for col in ["part_femmes_2012", "part_femmes_2023", "variation_absolue"]:
    evo_display[col] = evo_display[col].round(2)

st.dataframe(evo_display.head(top_n), width="stretch")


#Série temporelle : évolution annuelle
st.subheader("Évolution annuelle (sélection)")

curve = evol[evol["nom_fed"] == fed].sort_values("year")

fig = px.line(
    curve,
    x="year",
    y="part_femmes",
    markers=True,
    title=f"Part des femmes — {fed}"
)
fig.update_layout(
    xaxis_title="Année",
    yaxis_title="Part des femmes (%)"
)

st.plotly_chart(fig, width="stretch")
