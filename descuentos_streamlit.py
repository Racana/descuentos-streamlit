import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import boto3
import os
from io import StringIO

st.sidebar.title('Descuentos disponibles en Buenos Aires')
st.sidebar.markdown(
    """
Datos obtenidos desde los sitios webs de Movistar, San Lorenzo y Swiss Medical Group mediante web scrapping para uso educacional.
Los datos muestran los distintos descuentos ofrecidos al 25 de Abril del 2020
    """
)

@st.cache
def call_data():
    df = pd.read_csv('https://storage.googleapis.com/descuentos-streamlit/df.csv')
    return df
    
data = call_data()

option_site = st.multiselect(
    'Pagina',
    data['Pagina'].unique()
)

option_cat = st.multiselect(
    'Categoria',
    data['Categoria'].sort_values().unique()
)

if not option_cat:
    filtered_data = data[
        data['Pagina'].isin(option_site)
        ]
else:
    filtered_data = data[
        (data['Pagina'].isin(option_site)) & 
        (data['Categoria'].isin(option_cat))
        ]

st.write(filtered_data[['Titulo', 'Descuento', 'Pagina']].to_html(escape=False, index=False), unsafe_allow_html=True)