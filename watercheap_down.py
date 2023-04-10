#!/usr/bin/env python
# coding: utf-8

# In[12]:


import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import streamlit as st
from streamlit_folium import folium_static
import folium

st.set_page_config(page_title='Water Consumption App')

# load or create leaderboard
try:
    leaderboard_df = pd.read_csv('leaderboard.csv')
except FileNotFoundError:
    leaderboard_df = pd.DataFrame({'Contributor': [], 'Points': []})

# load or create water consumption data
try:
    data_df = pd.read_csv('data.csv')
except FileNotFoundError:
    data_df = pd.DataFrame({'Contributor': [], 'Latitude': [], 'Longitude': [], 'Consumption': []})

# display leaderboard
st.header('Leaderboard')
if leaderboard_df.empty:
    st.write('No contributors yet.')
else:
    st.dataframe(leaderboard_df.sort_values(by='Points', ascending=False))

# display map
st.header('Water Consumption Map')
st.subheader('Add data point')
contributor = st.text_input('Enter your name')
lat = st.number_input('Enter latitude', value=0.0,step=0.0001, format="%.6f")
lon = st.number_input('Enter longitude', value=0.0,step=0.0001, format="%.6f")
consumption = st.number_input('Enter consumption', value=0)

if st.button('Add'):
    # add data to dataframe
    data_df = data_df.append({'Contributor': contributor, 'Latitude': lat, 'Longitude': lon, 'Consumption': consumption}, ignore_index=True)
    data_df.to_csv('data.csv', index=False)

    # update points for contributor
    points = 0
    if not data_df[(data_df['Latitude'] == lat) & (data_df['Longitude'] == lon)].empty:
        points += 1

    if contributor in leaderboard_df['Contributor'].values:
        leaderboard_df.loc[leaderboard_df['Contributor'] == contributor, 'Points'] += points
    else:
        leaderboard_df = leaderboard_df.append({'Contributor': contributor, 'Points': points}, ignore_index=True)

    leaderboard_df.to_csv('leaderboard.csv', index=False)

    st.success('Data added!')

    # display updated leaderboard
    st.header('Leaderboard')
    st.dataframe(leaderboard_df.sort_values(by='Points', ascending=False))

# display map
if data_df.empty:
    st.write('No data yet.')
else:
    # create map with markers for each data point
    mapbox_token = 'pk.eyJ1IjoiYXJ0aHVyc3J6IiwiYSI6ImNsZzFnYXVhajF1b2wzcXF1NDk0YzloMDcifQ.pCcmmYpxXDGzTUQWoBxsCA'
    m = folium.Map(location=[data_df['Latitude'].mean(), data_df['Longitude'].mean()], zoom_start=5, tiles="CartoDB positron", width='100%', height='80%')
    for i, row in data_df.iterrows():
        folium.Marker([row['Latitude'], row['Longitude']]).add_to(m)
    folium_static(m)

