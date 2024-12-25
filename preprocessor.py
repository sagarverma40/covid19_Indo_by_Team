import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
# Function to create filter multiselect options in Streamlit
def multiselect(title, options_list):
    selected = st.sidebar.multiselect(title, options_list)
    select_all = st.sidebar.checkbox("Select all", value=True, key=title)
    if select_all:
        selected_options = options_list
    else:
        selected_options = selected
    return selected_options

# Pie chart showing infection percentage in a region

def plot_location_wise_infection_pie(filtered_df):
    """
    This function creates and displays pie charts for each location showing 
    the percentage of people infected by COVID and non-infected, arranged as subplots.

    Args:
    filtered_df: DataFrame containing 'Location', 'Total Cases', and 'Population' columns.
    """
    # Group by Location and sum up the Total Cases (no need to sum Population)
    location_grouped = filtered_df.groupby(['Location', 'Year']).agg({
        'Total Cases': 'sum', 
        'Population': 'first'  # Population is the same for a location, so we take the first value
    }).reset_index()

    # Calculate the Infected Percentage for each location
    location_grouped['Infected Percentage'] = location_grouped.apply(
        lambda row: (row['Total Cases'] / row['Population'] * 100) if row['Population'] > 0 else 0,
        axis=1
    )

    # Get the unique locations
    locations = location_grouped['Location'].unique()

    # Set up the figure for subplots (3 pie charts per row)
    n_cols = 3  # We want 3 pie charts per row
    n_rows = len(locations) // n_cols + (1 if len(locations) % n_cols != 0 else 0)
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, n_rows * 5))
    
    # Flatten axes for easy iteration
    axes = axes.flatten()

    for i, location in enumerate(locations):
        # Filter data for the current location
        location_data = location_grouped[location_grouped['Location'] == location]
        
        # Calculate the percentage of infected and non-infected people
        infected_percentage = location_data['Infected Percentage'].iloc[0]
        non_infected_percentage = 100 - infected_percentage  # Remaining percentage
        
        # Ensure there are no negative values (just in case)
        infected_percentage = max(infected_percentage, 0)
        non_infected_percentage = max(non_infected_percentage, 0)
        
        # Prepare data for the pie chart
        data = ['Infected', 'Non-Infected']
        percentages = [infected_percentage, non_infected_percentage]

        # Select axis for the current subplot
        ax = axes[i]

        # Create the pie chart
        ax.pie(percentages, labels=data, autopct='%1.1f%%', startangle=90, colors=['#FF5733', '#C1C1C1'])
        ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.

        # Add a title with the location name
        ax.set_title(f'{location}')
    
    # Remove any empty subplots (if number of locations isn't divisible by 3)
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    # Display the pie charts in Streamlit
    st.pyplot(fig)


# Heatmap to show a correlation between population density and total covid cases

def plot_total_cases_population_density_heatmap(filtered_df):
    """
    Creates and displays a heatmap showing the relationship between
    Total Cases and Population Density for different Locations.
    """
    # Step 1: Prepare the data
    heatmap_data = filtered_df[['Location', 'Population Density', 'Total Cases']].dropna()

    # Ensure valid numerical data for Population Density and Total Cases
    heatmap_data = heatmap_data[heatmap_data['Population Density'] > 0]  # Filter rows where Population Density > 0

    # Step 2: Pivot the data for the heatmap
    heatmap_pivot = heatmap_data.pivot_table(
        values='Total Cases',
        index='Location',
        columns='Population Density',
        aggfunc='sum',
        fill_value=0  # Replace NaN with 0 if needed
    )

    # Step 3: Create the heatmap using Seaborn
    fig, ax = plt.subplots(figsize=(14, 10))  # Adjust size as needed
    sns.heatmap(heatmap_pivot, annot=True, fmt='g', cmap='coolwarm', cbar=True, ax=ax)
    ax.set_title('Heatmap: Total Cases vs Population Density by Location', fontsize=16)
    ax.set_xlabel('Population Density', fontsize=12)
    ax.set_ylabel('Location', fontsize=12)

    # Step 4: Render the heatmap in Streamlit
    st.pyplot(fig)