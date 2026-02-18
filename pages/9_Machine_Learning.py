import numpy as np
import scipy
import streamlit as st
from scipy.interpolate import Akima1DInterpolator
import ML_function as mlf
import app as mn
import plotly.express as px

data1=mn.data1

fed = st.selectbox("Select a fed you want to see preds", 
                   data1["nom_fed"].sort_values().unique())
year = 2026
#st.selectbox("Select a year you want to see your pred",
        #            data1["year"].sort_values().unique())



df_filtered=data1[data1["nom_fed"]==fed]
try:
    df_future_pred = mlf.LinReg(df_filtered, year)

    

    st.write(f"Prediction for {year}:",year)
    st.write("Future predictions:")
    st.dataframe(df_future_pred)



    x=df_future_pred["year"]
    y=df_future_pred["total_lic"]

    xs = np.linspace(min(x), max(y),num=100)
    y_akima = Akima1DInterpolator(x, y, method="akima")(xs)

    #st.line_chart(xs, x="x")
    fig = px.line(df_future_pred, x="year", y="total_lic", title='pred')
    st.plotly_chart(fig, use_container_width=True)
except:
    st.write("Data insuffisante pour "+fed)