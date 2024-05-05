import streamlit as st
import pandas as pd
import plotly_express as px
df = pd.read_csv('vehicles_us.csv')
st.header('Data Viewer')
st.dataframe(df)
st.header('Relationship Between Car Price / Quality and Days Listed')
fig_scatter = px.scatter(df, x='price', y='days_listed', color='condition', labels={'price':'Car Price', 'days_listed':'Number of Days Listed'})
st.write(fig_scatter)
st.header('Price compared by Manufacturer')
fig_hist2 = px.histogram(df, x='price', color="manufacturer", nbins=75)
st.write(fig_hist2)
st.header('Relationship Between Car Price / Mileage')
fig_scatter2 = px.scatter(df, x='odometer', y='price')
st.write(fig_scatter2)
st.header('Condition vs Year')
condition_list = sorted(df['condition'].unique())
year_list = sorted(df['model_year'].unique())
Condition = st.selectbox(
    label='Select Condition Type',
    options=condition_list,
    index=condition_list.index('good')
)
year = st.selectbox(
    label='Select Year',
    options=year_list,
    index=year_list.index('2020')
)
normalize = st.checkbox('Normalize Histogram', value=True)
if normalize:
    histnorm = 'percent'
else:
    histnorm = None
fig_hist1 = px.histogram(df, x='model_year', color="condition", nbins=75, histnorm=histnorm)
st.write(fig_hist1)
