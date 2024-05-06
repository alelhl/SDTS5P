import streamlit as st
import pandas as pd
import plotly.express as px
df = pd.read_csv('vehicles_us.csv')
df['manufacturer'] = df['model'].str.split().str[0]
df = df.reindex(['model_year', 'manufacturer', 'model', 'price', 'condition', 'cylinders', 'fuel', 'odometer', 'transmission', 'type', 'paint_color', 'is_4wd', 'date_posted', 'days_listed'], axis = 1)
df['model_year'] = df['model_year'].fillna(df.groupby(["manufacturer"])['model_year'].transform(lambda x: x.fillna(x.median())))
df['model_year'] = df['model_year'].astype(int)
df['cylinders'] = df['cylinders'].fillna(df.groupby(["manufacturer"])['cylinders'].transform(lambda y: y.fillna(y.median())))
df['cylinders'] = df['cylinders'].astype(int)
df['odometer'] = df['odometer'].fillna(df.groupby(["model_year"])['odometer'].transform(lambda z: z.fillna(z.mean())))
df['odometer'] = round(df['odometer'])
df['odometer'] = df['odometer'].astype(int, errors='ignore')
df['paint_color'] = df['paint_color'].fillna('none')
df['is_4wd'] = df['is_4wd'].fillna(0.0)
df['date_posted'] = pd.to_datetime(df['date_posted'])
model_year_Q1 = df['model_year'].quantile(0.25)
model_year_Q3 = df['model_year'].quantile(0.75)
model_year_IQR = model_year_Q3 - model_year_Q1
threshold = 1.5
model_year_outliers = df[(df['model_year'] < model_year_Q1 - threshold * model_year_IQR) | (df['model_year'] > model_year_Q3 + threshold * model_year_IQR)]
price_Q1 = df['price'].quantile(0.25)
price_Q3 = df['price'].quantile(0.75)
price_IQR = price_Q3 - price_Q1
threshold = 1.5
price_outliers = df[(df['price'] < price_Q1 - threshold * price_IQR) | (df['price'] > price_Q3 + threshold * price_IQR)]
odometer_Q1 = df['odometer'].quantile(0.25)
odometer_Q3 = df['odometer'].quantile(0.75)
odometer_IQR = odometer_Q3 - odometer_Q1
threshold = 1.5
odometer_outliers = df[(df['odometer'] < odometer_Q1 - threshold * odometer_IQR) | (df['odometer'] > odometer_Q3 + threshold * odometer_IQR)]
df['odometer'] = df['odometer'].drop(odometer_outliers.index)
df['price'] = df['price'].drop(price_outliers.index)
df['model_year'] = df['model_year'].drop(model_year_outliers.index)
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
condition = st.selectbox(
    label='Select Condition Type',
    options=condition_list,
    index=condition_list.index('good')
)

mask_filter = (df['condition'] == condition)
df_filtered = df[mask_filter]
normalize = st.checkbox('Normalize Histogram', value=True)
if normalize:
    histnorm = 'percent'
else:
    histnorm = None
fig_hist1 = px.histogram(df_filtered, x='model_year', color="condition", nbins=75, histnorm=histnorm)
st.write(fig_hist1)
