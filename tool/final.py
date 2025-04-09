# Importing Libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

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

st.markdown("### 1. Footfall of customers by Hour")

# Set consistent day order
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Add day name column
df['Day_name'] = df.index.day_name()

# Count number of transactions per date
daily_counts = df.groupby([df.index.date, 'Day_name'])['transaction_id'].count().reset_index()
daily_counts.columns = ['Date', 'Day_name', 'Bills']

# Average per weekday
avg_daily_footfall = daily_counts.groupby('Day_name')['Bills'].mean().reindex(day_order)

# Plot
col1, col2, col3 = st.columns


fig = px.bar(x=avg_daily_footfall.index, y=avg_daily_footfall.values, title="Footfall by Day")
st.plotly_chart(fig, use_container_width=True)