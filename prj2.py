#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Import necessary libraries
import pandas as pd
import streamlit as st
import plotly.express as px

# Load the financial data
data = pd.read_csv('financials.csv')

# Remove leading and trailing whitespaces from column names
data.columns = data.columns.str.strip()

# Sidebar widgets
st.sidebar.header('Filter Data')
selected_products = st.sidebar.multiselect('Select Products:', data['Product'].unique())
selected_segments = st.sidebar.multiselect('Select Segments:', data['Segment'].unique())
selected_year_range = st.sidebar.slider('Select Year Range:', data['Year'].min(), data['Year'].max(), (data['Year'].min(), data['Year'].max()))

# Use the selected products, segments, and year range to filter data
filtered_data = data[(data['Product'].isin(selected_products)) & 
                     (data['Segment'].isin(selected_segments)) & 
                     (data['Year'] >= selected_year_range[0]) & 
                     (data['Year'] <= selected_year_range[1])]

# Set background color using HTML styling
background_color = """
    <style>
        body {
            background-color: #f0f0f0;  /* Set your desired background color */
        }
    </style>
"""
st.markdown(background_color, unsafe_allow_html=True) 

# Dashboard title
if selected_products or selected_segments or selected_year_range:
    title_text = 'Financial Analysis'
    if selected_products:
        title_text += f' - Products: {", ".join(selected_products)}'
    if selected_segments:
        title_text += f' - Segments: {", ".join(selected_segments)}'
    if selected_year_range:
        title_text += f' - Year Range: {selected_year_range[0]} to {selected_year_range[1]}'
    st.title(title_text)
else:
    st.title('Financial Analysis')

# Group by 'Month Number' and aggregate sales
aggregated_data = filtered_data.groupby('Month Number')['Sales'].sum().reset_index()

# Line chart with aggregated data
st.header('Total Revenue Over Time')
fig1 = px.line(aggregated_data, x='Month Number', y='Sales', title='Total Revenue Over Time')
st.plotly_chart(fig1)

st.header('Profit vs. Revenue')
fig3 = px.scatter(filtered_data, x='Sales', y='Profit')
st.plotly_chart(fig3)

st.header('Revenue Distribution by Product')
fig4 = px.box(filtered_data, x='Product', y='Sales')
st.plotly_chart(fig4)

st.header('Country Wise Profit Distribution')
fig5 = px.pie(filtered_data, values='Profit', names='Country', title='Country Wise Profit Distribution')
st.plotly_chart(fig5)

# Histogram for Cost Distribution with black boundaries
st.header('Cost Distribution')
fig6 = px.histogram(filtered_data, x='COGS', nbins=30, title='Cost Distribution', 
                    opacity=0.7, # Set the opacity of bars
                    barmode='overlay', # Overlay histograms
                    barnorm='percent', # Normalize to percentage
                    histnorm='probability density') # Normalize to probability density

# Update trace to add black boundaries
fig6.update_traces(marker=dict(color='blue', line=dict(color='black', width=1.5)))

st.plotly_chart(fig6)
