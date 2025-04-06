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


# df['daily_sales'] = df['transaction_qty'].resample('D').sum()
# df['daily_summary'] = df.resample('D').agg({
#     'transaction_qty': 'sum',
#     'revenue': 'sum'
# })

# df['hourly_avg'] = df.groupby('Hour')['transaction_qty'].mean()

# Show dataframe preview
st.dataframe(df.head())

# Column selection
st.markdown("### Select Columns for Plot")
numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
all_cols = df.columns.tolist()

col1 = st.selectbox("Select X-axis Column", all_cols, index=0)
col2 = st.selectbox("Select Y-axis Column", numeric_cols, index=1)

# Plot type
st.markdown("### Select Plot Type")
plot_type = st.selectbox("Choose Plot Type", ["Line Plot", "Bar Plot"])

# Button to generate plot
if st.button("Generate Plot"):
    fig, ax = plt.subplots(figsize=(12, 6))

    if plot_type == "Line Plot":
        sns.lineplot(data=df, x=col1, y=col2, ax=ax)
        plt.title(f"Line Plot of {col2} vs {col1}")
        plt.xticks(rotation=45)

    elif plot_type == "Bar Plot":
        # Group by X and aggregate Y if needed
        bar_data = df.groupby(col1)[col2].sum().reset_index()
        sns.barplot(data=bar_data, x=col1, y=col2, ax=ax)
        plt.title(f"Bar Plot of {col2} grouped by {col1}")
        plt.xticks(rotation=45)

    st.pyplot(fig)