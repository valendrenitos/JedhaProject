fed = st.selectbox("Select a fed you want to see preds", 
                   data1["nom_fed"].sort_values().unique())
year = st.selectbox("Select a year you want to see your pred",
                    data1["year"].sort_values().unique())

data1=load_data()

df_filtered=data1[data1["nom_fed"]==fed]

selected_pred, df_future_pred = LinReg(df_filtered, year)

st.write(f"Prediction for {year}:", selected_pred)
st.write("Future predictions:")
st.dataframe(df_future_pred)

import numpy as np
import scipy
import streamlit as st


data = {"x": df_filtered["year"], "y": rng.random(N)}

interpolated = {"x": np.linspace(1, N-1, 100)}
interpolated["linear"] = np.interp(interpolated["x"], data["x"], data["y"])
interpolated["spline"] = scipy.interpolate.CubicSpline(data["x"], data["y"])(
    interpolated["x"]
)
interpolated["akima"] = scipy.interpolate.Akima1DInterpolator(data["x"], data["y"])(
    interpolated["x"]
)
interpolated["pchip"] = scipy.interpolate.PchipInterpolator(data["x"], data["y"])(
    interpolated["x"]
)

st.line_chart(interpolated, x="x")