import streamlit as st
import pandas as pd
import plotly.express as px
     
st.write("""
    # Fédé's data
    """)

#DATA_MEDIA_URL=('')


#Media data hist

@st.cache_data
def load_data(nrows):
    #data = pd.read_csv(DATA_MEDIA_URL,nrows=nrows)
    data=pd.read_csv("licenses_by_year_region_fed.csv")
    return data


data = load_data(20000)
st.write(data.head())

st.subheader("Licenciés par fédération")

with st.form("total_lics_par_fed"):
        fed = st.selectbox("Select a fed you want to see lics", data["nom_fed"].sort_values().unique())
        year = st.selectbox("Select a year you want to see your metric", data["annee"].sort_values().unique())

        submit = st.form_submit_button("submit")

        if submit:
            # When the form is submitted, process user input and display results dynamically
            
            mask = data[(data["nom_fed"] == fed)& (data["annee"] == year)]
            total_lic_fed = mask["total_license"].sum()

            st.metric("Total lic per fed", total_lic_fed)
