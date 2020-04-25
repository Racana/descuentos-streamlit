import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import boto3
import os
from io import StringIO

@st.cache
def call_data():
    aws_id = os.environ.get('AWS_ID')
    aws_secret = os.environ.get('AWS_SK')
    client = boto3.client('s3', aws_access_key_id=aws_id,
            aws_secret_access_key=aws_secret)
    bucket_name = 'descuentos-argentina-bucket'
    object_key = 'df.csv'
    csv_obj = client.get_object(Bucket=bucket_name, Key=object_key)
    body = csv_obj['Body']
    csv_string = body.read().decode('utf-8')
    data = pd.read_csv(StringIO(csv_string), index_col=0)
    return data

data = call_data()

st.title('Descuentos disponibles en Buenos Aires')

option_site = st.multiselect(
    'Pagina',
    data['Pagina'].unique()
)

option_cat = st.multiselect(
    'Categoria',
    data['Categoria'].unique()
)

filtered_data = data[(data['Pagina'].isin(option_site)) &
                (data['Categoria'].isin(option_cat))]
st.write(filtered_data[['Titulo', 'Descuento', 'Pagina']].to_html(escape=False, index=False), unsafe_allow_html=True)


#& (data['Categoria'] == option_cat)
#st.subheader('Map of all pickups at %s:00' % hour_to_filter)
