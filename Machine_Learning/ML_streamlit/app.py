import numpy as np
import scipy
import streamlit as st
from scipy.interpolate import Akima1DInterpolator
import ML_function

fed = st.selectbox("Select a fed you want to see preds", 
                   data1["nom_fed"].sort_values().unique())
year = st.selectbox("Select a year you want to see your pred",
                    data1["year"].sort_values().unique())

#data1=load_data()

df_filtered=data1[data1["nom_fed"]==fed]

selected_pred, df_future_pred = LinReg(df_filtered, year)

st.write(f"Prediction for {year}:", selected_pred)
st.write("Future predictions:")
st.dataframe(df_future_pred)



data = {"x": df_filtered["year"], "y": df_filtered['total_lic']}

xs = np.linspace(min(x), max(x))
y_akima = Akima1DInterpolator(x, y, method="akima")(xs)

st.line_chart(interpolated, x="x")