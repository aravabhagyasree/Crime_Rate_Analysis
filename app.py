import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("Crime Analysis Dashboard - Karnataka")

df = pd.read_csv("/Users/bhagyasree/data_analytics/datafile.csv")

current = 'During the current month'
prev_month = 'During the previous month'
prev_year = 'During the corresponding month of previous year'

# Aggregate
major = df.groupby('Major Heads')[[current, prev_month, prev_year]].sum()

major['MoM_change'] = major[current] - major[prev_month]
major['YoY_change'] = major[current] - major[prev_year]

# Top crimes
st.subheader("Top Crime Categories")
st.bar_chart(major[current].sort_values(ascending=False).head(10))

# MoM
st.subheader("Month-over-Month Change")
st.bar_chart(major['MoM_change'].sort_values(ascending=False).head(10))

# YoY
st.subheader("Year-over-Year Change")
st.bar_chart(major['YoY_change'].sort_values(ascending=False).head(10))

# Heatmap
st.subheader("Crime Relationship Heatmap")

pivot = pd.pivot_table(
    df,
    values=current,
    index='Heads of Crime',
    columns='Major Heads',
    aggfunc='sum'
).fillna(0)

fig, ax = plt.subplots(figsize=(10,5))
sns.heatmap(pivot, ax=ax)
st.pyplot(fig)