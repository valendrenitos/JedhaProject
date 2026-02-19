import plotly.express as px 
import plotly.graph_objects as go
import numpy as np
import pandas as pd

def graph_comparaison_media_lic(data1,event_coverage,data3,sport_events):
    
    data1=data1.groupby(["year"], as_index=False).agg(total_license=('total_lic','sum'))  
    
    
    data3read=data3[(data3["annee"]>2010) & (data3["annee"]<2025) ]
    datapred=data3[data3["annee"]>2023]
    
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data3read["annee"],
            y=data3read["total"],
            mode='lines+markers',
            name="Licences sportives",
            line=dict(color='royalblue', width=3),
            marker=dict(size=8),
            yaxis="y"          
        )
    )

    fig.add_trace(
        go.Scatter(
            x=datapred["annee"],
            y=datapred["total"],
            mode='lines+markers',
            name="Licenses supposées",
            line=dict(color='royalblue', width=3, dash='dash'),
            marker=dict(size=8),
            yaxis="y"          
        )
    )


    fig.add_trace(
        go.Scatter(
            x=data1["year"],               
            y=data1["total_license"],  
            mode='lines+markers',
            name="Licenses sportives uniques",
            line=dict(color='orange', width=2.5, dash='dash'),  
            marker=dict(size=7, symbol='diamond'),
            yaxis="y"                            
        )
    )

    fig.add_trace(
        go.Bar(
            x=event_coverage["year"],
            y=event_coverage["avrg_tv_aud"],
            name="Audience TV moyenne" + (" (selected events)" if len(sport_events)>0 else " (all events)"),
            marker_color='rgba(220, 80, 80, 0.65)',  
            yaxis="y2"                               
        )
    )


    fig.update_layout(
        title="COmparaison de l'évolution du nombre de licenses par rapport au nombre de téléspectateur moyen",
        xaxis_title="Année",
        
        
        yaxis=dict(
            title="licenses",
            
            tickfont=dict(color="royalblue"),
            side="left"
        ),

        yaxis2=dict(
            title="Téléspectateurs",
                    
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
    return fig



def graph_comparaison_media_lic_sex(data1, event_coverage):
 
    
    fig = go.Figure()

   
    fig.add_trace(
        go.Scatter(
            x=data1["year"],
            y=data1["total_f"],
            mode='lines+markers',
            name="Licences sportives féminine",
            line=dict(color='orange', width=2.5),
            marker=dict(size=7, symbol='diamond'),
            yaxis="y"
        )
    )

   
    fig.add_trace(
        go.Bar(
            x=event_coverage["year"],
            y=event_coverage["avrg_tv_aud"],
            name="Audience TV moyenne",
            marker_color='rgba(220, 80, 80, 0.65)',
            yaxis="y2"
        )
    )

    fig.update_layout(
        title="Évolution des licences sportives vs audience TV moyenne dans le sport féminin",
        xaxis_title="Année",
        
        yaxis=dict(
            title="Nombre de licences",
            tickfont=dict(color="orange"),
            side="left"
        ),
        
        yaxis2=dict(
            title="Téléspectateurs moyens",
            tickfont=dict(color="#d44"),
            overlaying="y",
            side="right"
        ),
        
        bargap=0.25,
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
    
    return fig