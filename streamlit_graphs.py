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




def graph_evolution_women_fed(df):
    # Préparation des données
    rolling_avg = (
        df.groupby(["nom_fed", "year"])["total_f"].sum() /
        df.groupby(["nom_fed", "year"])["total_lic"].sum()
    ).unstack("year").rolling(3, axis=1, min_periods=1).mean()

    df_long = (
        rolling_avg
        .mul(100)
        .rename_axis("federation")
        .reset_index()
        .melt(id_vars="federation", var_name="annee", value_name="part_femmes")
    )

    df_long["progression"] = (
        df_long.groupby("federation")["part_femmes"]
        .transform(lambda s: s - s.iloc[0])
    )

    fig = px.scatter(
        df_long,
        x="part_femmes",
        y="progression",
        animation_frame="annee",
        animation_group="federation",
        hover_name="federation",
        labels={
            "part_femmes": "Part de femmes (%)",
            "progression": "Progression depuis l'origine (points de %)",
            "annee": "Année"
        },
        title="Évolution de la féminisation par fédération",
        height=750
    )

    fig.add_vline(x=50, line_dash="dash", line_color="red", opacity=0.5)
    fig.add_hline(y=0, line_dash="dash", line_color="red", opacity=0.5)

    fig.update_xaxes(range=[0, 100])
    fig.update_yaxes(range=[-10, 35])

    return fig




def pie_chart(df):
    df.loc[(
        df["sport_event"]=="Roland Garros") & (df["year"]==2016),
        "genre"] = "mixte"


    

    data_pie = df.groupby("genre", as_index=False)["avrg_tv_aud"].sum()

    color_map = {
        "féminin": "#f59a53",
        "masculin": "#0e1f3a",
        "mixte": "#5a815c"
    }

    fig_target = go.Figure(data=[go.Pie(labels=data_pie["genre"],
                                        values=data_pie["avrg_tv_aud"],
                                        hole=.3,
                                        marker=dict(
                    colors=[color_map[g] for g in data_pie["genre"]])
                                    )])

    return fig_target