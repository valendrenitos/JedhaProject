import streamlit as st

st.set_page_config(
    page_title="Overview du Sport en France entre 2012 et 2023",
    layout="wide"
)
#page_title="Overview du Sport en France entre 2012 et 2023",

# flex = st.container(horizontal=True, horizontal_alignment="right")

# for card in range(3):
#     flex.button(f"Button {card + 1}")
if "page" not in st.session_state:
    st.session_state.page = "Accueil"

flex = st.container(horizontal=True, horizontal_alignment="right")

buttons = ["Overview du sport en France", "Médiatisation du sport", "Représentation des femmes"]

for name in buttons:
    if flex.button(name):
        st.session_state.page = name


st.title("Overview du Sport en France entre 2012 et 2023")

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
    max-width: 700px;
    margin-left: 150px;
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
