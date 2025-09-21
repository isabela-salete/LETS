import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import json
from unidecode import unidecode
import re

st.set_page_config(layout='wide')

st.title("Dados benefícios - 2023")

df = pd.read_csv('beneficios23.csv')
st.dataframe(df)
