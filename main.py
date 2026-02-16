import pandas as pd
import streamlit as st 
import plotly.express as px 
import plotly.graph_objects as go
import numpy as np

from DBConnector import getData


st.set_page_config(
    page_title="Projet Final jedha DAFS-16",
    page_icon="💸 ",
    layout="wide"
)
@st.cache_data
def load_data():
    data1,data2,data3=getData()
    
    
    
    return data1,data2,data3 

data1,data2,data3=load_data()

datatreated1=data1.groupby(["year"], as_index=False).agg(total_license=('total_lic','sum'))

# DATA 1 : LICENSES : COLONNES : year,  region,  nom_fed, total_lic, total_f, total_h, h_1_9, h_10_19, h_20_29,h_30_59,h_60_74, h_75, f_1_9, f_10_19, f_20_29, f_30_59, f_60_74, f_75
# DATA 2 : Medias : sport_event,sport,year,avrg_tv_aud,avrg_tv_match,total_match,hours_live,numb_of_post
# DATA 3 Club 49-23 : annee,  olympics,  non_olympics, affinitaire, scholair, total

st.subheader("Problématique")

st.markdown("""
    Mettre la problématique ici
""")

sport_events= st.multiselect("Select sportive events", 
                             data2["year"].sort_values().unique(), 
                             placeholder=None,
                             label_visibility="visible", 
                             accept_new_options=False, 
                             width="stretch")

if len(sport_events)>0:
    event_coverage= data2[data2["sport_event"].isin(sport_events)]
else:
    event_coverage=data2

# fig = px.line(x=datatreated1["year"], y=datatreated1["total_license"], color=px.Constant("This year"),
#              labels=dict(x="année", y="licenses", color="Time Period"))
# fig.add_bar(event_coverage, 
#                  x = "annee", 
#                  y="avrg_tv_aud",
#                  name= "Average TV coverage for selected events" if len(sport_events)>0 else "Average TV coverage for all events",
#                  color="sport")
# fig.update_layout(bargap=0.2)
data3read=data3[data3["annee"]>2010]

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=data3read["annee"],
        y=data3read["total"],
        mode='lines+markers',
        name="This year - Total licenses",
        line=dict(color='royalblue', width=3),
        marker=dict(size=8),
        yaxis="y"          
    )
)


fig.add_trace(
    go.Scatter(
        x=datatreated1["year"],               
        y=datatreated1["total_license"],  
        mode='lines+markers',
        name="Last year - Total licenses",
        line=dict(color='orange', width=2.5, dash='dash'),  
        marker=dict(size=7, symbol='diamond'),
        yaxis="y"                            
    )
)

fig.add_trace(
    go.Bar(
        x=event_coverage["year"],
        y=event_coverage["avrg_tv_aud"],
        name="Avg TV audience" + (" (selected events)" if len(sport_events)>0 else " (all events)"),
        marker_color='rgba(220, 80, 80, 0.65)',  
        yaxis="y2"                               
    )
)


fig.update_layout(
    title="Total licenses vs Average TV audience per year",
    xaxis_title="Année",
    
    
    yaxis=dict(
        title="Total licenses",
        
        tickfont=dict(color="royalblue"),
        side="left"
    ),

    yaxis2=dict(
        title="Average TV audience",
                 
        tickfont=dict(color="#d44"),
        overlaying="y",
        side="right"
    ),
    
    bargap=0.25,
    barmode='overlay',
    hovermode="x unified",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    template="plotly_white"  
)
st.plotly_chart(fig, use_container_width='stretch')



