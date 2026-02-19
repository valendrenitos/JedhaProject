import streamlit as st
import pandas as pd
import plotly.express as px
import app as mn
from utils import sidebar_filters, apply_filters

df = mn.data1
f = sidebar_filters(df)
dff = apply_filters(df, f)

st.title("Analyse par fédération sportive")
