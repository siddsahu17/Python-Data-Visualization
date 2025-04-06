# Importing Libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="BTD Visualization Tool", layout="wide")

# Title
st.title("Visualization Tool")



df = pd.read_csv('../data/Coffee Shop Sales.csv')
df['date'] = df['transaction_date'] + '-' +  df['transaction_time']
df.drop(['transaction_date', 'transaction_time'], axis=1, inplace=True)
df['date'] = pd.to_datetime(df['date'], format = "mixed")
df.set_index('date', inplace=True)
st.success("Data Loaded Successfully!")

# EDA on Data
df['Month'] = df.index.month
df['Day'] = df.index.day
df['Day_name'] = df.index.day_name()

df['is_weekend'] = df.index.weekday > 4

df['Hour'] = df.index.hour

df['revenue'] = df['transaction_qty'] * df['unit_price']

# Show dataframe preview
st.dataframe(df.head())


df['daily_sales'] = df['transaction_qty'].resample('D').sum()

df['hourly_avg'] = df.groupby('Hour')['transaction_qty'].mean()

# Plots for my visualization tool