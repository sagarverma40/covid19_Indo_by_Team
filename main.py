import pandas as pd
import plotly.express as px
import streamlit as st
import altair as alt
import preprocessor

df=pd.read_csv('Covid19_Indonesia.csv')



# Title for Dashboard
st.sidebar.title('Filters')
st.markdown("<h1 style='text-align: center;'>Indonesia: COVID-19 Analytics Dashboard</h1>", unsafe_allow_html=True)
# Path to your image (make sure the path is correct)
file_path = r'/Users/dheerajkumar/Desktop/Screenshot 2024-12-18 at 11.10.08.png'
st.image(file_path)



# Filters
selected_location= preprocessor.multiselect('Select Location',df['Location'].unique())
selected_year=preprocessor.multiselect('Select Year',df['Year'].unique())
selected_month=preprocessor.multiselect('Select Month',sorted(df['Month'].unique()))
selected_day=preprocessor.multiselect('Select Day',sorted(df['Day'].unique()))

filtered_df=df[(df['Year'].isin(selected_year)) &
               (df['Month'].isin(selected_month)) &
               (df['Day'].isin(selected_day)) &
               (df['Location'].isin(selected_location))]

#KPI - Key Performance indicator

# Create columns for displaying KPIs
col1,col2=st.columns(2)

# Total Covid Cases
with col1:
    st.metric(label='Total Covid Cases',value= f'{int(filtered_df['Total Cases'].sum())}')

# Total Active Cases
with col2:
    st.metric(label='Total Active Cases',value= f'{int(filtered_df['Total Active Cases'].sum())}')
col3,col4=st.columns(2)
    
# Total Recovered
with col3:
    st.metric(label='Total Recovered',value= f'{int(filtered_df['Total Recovered'].sum())}')
    
# Total Deaths
with col4:
    st.metric(label='Total Deaths',value= f'{int(filtered_df['Total Deaths'].sum())}')

# Visualization to analyze yearly Covid trends
col5=st.columns(1)[0]
with col5:
    st.subheader('Total Covid Cases Yearly')
# Group the data by 'Year' and sum the required columns
    Covid_trend = (filtered_df.groupby('Year')['Total Cases']
                   .sum())                   
# Create a bar chart with Altair (you can adjust the figsize by setting width and height)
    bar_chart = alt.Chart(Covid_trend.reset_index()).mark_bar().encode(
        x='Year:N',  # X-axis as Year (categorical)
        y='Total Cases:Q',  # Y-axis as Total Cases (quantitative)
        color='Year:N'  # Color by Year to distinguish
    ).properties(
        width=750,  # Adjust width (figsize)
        height=500  # Adjust height (figsize)
    )
    # Display the bar chart using Streamlit
    st.altair_chart(bar_chart)
    
# Top Provinces by Total Cases
st.subheader("Top Provinces by Total Cases")
top_provinces = filtered_df.groupby("Province")["Total Cases"].max().nlargest(10)
st.bar_chart(top_provinces)

# Pie chart showing infection percentage in a region

from preprocessor import plot_location_wise_infection_pie

# Call the function to plot the pie charts
plot_location_wise_infection_pie(filtered_df)

# Group the data by 'Location' and sum the required columns
location_total_cases = filtered_df.groupby('Location')['Total Cases'].sum().sort_values(ascending=False)
location_active_cases = filtered_df.groupby('Location')['Total Active Cases'].sum().sort_values(ascending=False)
location_total_deaths = filtered_df.groupby('Location')['Total Deaths'].sum().sort_values(ascending=False)
location_total_recovered = filtered_df.groupby('Location')['Total Recovered'].sum().sort_values(ascending=False)

# Define the color scale (use a valid Vega color scheme like 'tableau10')
color_scale = alt.Scale(domain=location_total_cases.index.tolist(), range=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'])

# Pie Chart for Location & Population Density
st.subheader("Location and its Population density")
pie_chart = alt.Chart(filtered_df.groupby('Location')['Population Density'].mean().reset_index()).mark_arc().encode(
    theta='Population Density:Q',  # Size of each slice
    color=alt.Color('Location:N', scale=color_scale),  # Use consistent color scale
    tooltip=['Location:N', 'Population Density:Q']  # Tooltip showing Location and Total Active Cases
).properties(
    
    width=700,
    height=400
)
# Display the pie chart in Streamlit
st.altair_chart(pie_chart)
pie_data = filtered_df.groupby('Location')['Population Density'].mean().reset_index()

# Heatmap to show a correlation between population density and total covid cases
from preprocessor import plot_total_cases_population_density_heatmap
# Call the function to generate and display the heatmap
plot_total_cases_population_density_heatmap(filtered_df)



# Chart 1: Location-wise Total Covid Cases

col1 = st.columns(1)[0]
with col1:
    st.subheader("Location-wise Total Covid Cases")
    bar_chart = alt.Chart(location_total_cases.reset_index()).mark_bar().encode(
        x='Location:N',
        y='Total Cases:Q',
        color=alt.Color('Location:N', scale=color_scale),
        tooltip=['Location:N', 'Total Cases:Q']
    ).properties(width=700, height=400)
    st.altair_chart(bar_chart)

col2 = st.columns(1)[0]
# Chart 2: Location-wise Total Active Cases
with col2:
    st.subheader("Location-wise Total Active Covid Cases")
    bar_chart = alt.Chart(location_active_cases.reset_index()).mark_bar().encode(
        x='Location:N',
        y='Total Active Cases:Q',
        color=alt.Color('Location:N', scale=color_scale),
        tooltip=['Location:N', 'Total Active Cases:Q']
    ).properties(width=700, height=400)
    st.altair_chart(bar_chart)

# Chart 3: Location-wise Total Death Cases
col3 = st.columns(1)[0]

with col3:
    st.subheader("Location-wise Total Death Cases")
    bar_chart = alt.Chart(location_total_deaths.reset_index()).mark_bar().encode(
        x='Location:N',
        y='Total Deaths:Q',
        color=alt.Color('Location:N', scale=color_scale),
        tooltip=['Location:N', 'Total Deaths:Q']
    ).properties(width=700, height=400)
    st.altair_chart(bar_chart)

col4 = st.columns(1)[0]

# Chart 4: Location-wise Total Recovered Cases
with col4:
    st.subheader("Location-wise Total Recovered Cases")
    bar_chart = alt.Chart(location_total_recovered.reset_index()).mark_bar().encode(
        x='Location:N',
        y='Total Recovered:Q',
        color=alt.Color('Location:N', scale=color_scale),
        tooltip=['Location:N', 'Total Recovered:Q']
    ).properties(width=700, height=400)
    st.altair_chart(bar_chart)







