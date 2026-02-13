import streamlit as st
import pandas as pd
import plotly.express as px
     
st.write("""
    # Histogramme media data
    """)

#DATA_MEDIA_URL=('')


#Media data hist

@st.cache_data
def load_data(nrows):
    #data = pd.read_csv(DATA_MEDIA_URL,nrows=nrows)
    data=pd.read_csv("Data media - Evenements sportifs.csv")
    data=data.rename(columns=
                {"évènement": "event",
                  "année": "year", 
                  "audience TV moynne total event":"global_tv_coverage_avg", 
                  "audience TV moy par match" : "match_tv_coverage_avg", 
                  "Nombre de matchs" : "matchs_nb" })
    data["year"]= pd.to_datetime(data["year"], format="%Y")
    data=data.drop(columns=["nombre de posts RS","heures d'antenne (télévision linéaire)"])
    data['sport']=data["sport"].fillna("multi")
    return data


data = load_data(30)
st.write(data.head())

sport_events= st.multiselect("Select sportive events", 
                             data["event"].sort_values().unique(), 
                             placeholder=None,
                             label_visibility="visible", 
                             accept_new_options=False, 
                             width="stretch")

if len(sport_events)>0:
    event_coverage= data[data["event"].isin(sport_events)]
else:
    event_coverage=data


fig=px.histogram(event_coverage, 
                 x = "event", 
                 y="global_tv_coverage_avg",
                 title= "Average TV coverage for selected events" if len(sport_events)>0 else "Average TV coverage for all events",
                 color="sport")

st.plotly_chart(fig, use_container_width='stretch')



#EDA Total lics par fédé

st.subheader("Licenciés par fédération")

    with st.form("total_lics_par_fed"):
        fed = st.selectbox("Select a fed you want to see lics", data["nom_fed"].sort_values().unique())
        year = st.selectbox("Select a year you want to see your metric", data["annee"].sort_values().unique())

        submit = st.form_submit_button("submit")

        if submit:
            # When the form is submitted, process user input and display results dynamically
            
            mask = data[(data["nom_fed"] == fed)& (data["annee"] == year)]
            total_lic_fed = mask["total_lic"].sum()

            st.metric("Total lic per fed", total_lic_fed)
