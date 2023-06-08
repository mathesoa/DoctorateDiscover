import folium
from folium.plugins import MarkerCluster
from branca.colormap import LinearColormap, StepColormap
import pandas as pd
from folium.features import DivIcon
import seaborn as sns

def world_rank_map(df):
    # Define a colormap based on the rank values
    ranks = df['rank']
    colorblind_friendly_colors = ['#4A90E2', '#50E3C2', '#F5A623', '#D0021B', '#9013FE']
    cmap = LinearColormap(
        colorblind_friendly_colors,
        vmin=ranks.min(), vmax=ranks.max(),
    )
    # Create a map object
    m = folium.Map(location=[20, -20], zoom_start=1.5)
    
    def custom_title(text):
        return ' '.join([word.title() if len(word) > 2 else word for word in text.split()])
    df['name'] = df['name'].apply(custom_title)
   
    # Add markers for each school to the map
    for i, row in df.iterrows():
        rank = row['rank']
        location = (row['Latitude'], row['Longitude'])
        popup_text = f"{row['name']}:{rank}"
        # Add a CircleMarker to the map
        circle_marker = folium.CircleMarker(
            location=location,
            radius=5,
            fill=True,
            color=cmap(rank),
            fill_opacity=0.7,
            fill_color=cmap(rank),
            popup=popup_text
        )
        circle_marker.add_to(m)

    # Add the colormap to the map
    cmap.caption = 'School Rank'
    cmap.add_to(m)

    # Return the map object
    return m
    


def phd_select_map(df, criteria):
    # Define a colormap based on the criteria values
    values = df[criteria].sort_values()
    colorblind_friendly_colors = ['#4A90E2', '#50E3C2', '#F5A623', '#D0021B', '#9013FE']
    cmap = LinearColormap(
        colorblind_friendly_colors,
        vmin=values.min(), vmax=values.max(),
    )

    # Create a map object 
    m = folium.Map(location=[30, -95], zoom_start=3.5)

    # Remove duplicates based on location and study_name
    df = df.drop_duplicates(subset=['LATITUDE', 'LONGITUDE', 'University'])

    # Add markers for each school to the map
    for i, row in df.iterrows():
        value = row[criteria]
        location = (row['LATITUDE'], row['LONGITUDE'])

        # Format criteria text
        criteria_text = ' '.join(word.capitalize() for word in criteria.split('_'))

        popup_text = f"{row['University']}: {criteria_text} {value}"

        # Add a CircleMarker to the map
        circle_marker = folium.CircleMarker(
            location=location,
            radius=5,
            fill=True,
            color=cmap(value),
            fill_opacity=0.7,
            fill_color=cmap(value)
        )
        circle_marker.add_to(m)
        
        # Add a Marker with DivIcon to the map
        marker = folium.Marker(
            location=location,
            icon=DivIcon(
                icon_size=(150, 36),
                icon_anchor=(7, -5),
                html=f'<div style="font-size: 10pt; color: black;">{popup_text}</div>',
            )
        )
        marker.add_to(m)

    # Add the colormap to the map
    cmap.caption = 'School Rank'
    cmap.add_to(m)

    # Return the map object
    return m


def remove_outliers(df, column):
    # Calculate Q1 and Q3
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    
    # Calculate the IQR
    IQR = Q3 - Q1
    
    # Define the lower and upper bounds
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # Remove outliers from the data
    df_no_outliers = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
    
    return df_no_outliers

def generate_box_plots(df, xcolumn, ycolumn, ax):
    # Convert column to numeric
    df[ycolumn] = pd.to_numeric(df[ycolumn], errors='coerce')

    df_no_outliers = remove_outliers(df, ycolumn)

    # Calculate average values for each x-value
    avg_values = df_no_outliers.groupby(xcolumn)[ycolumn].mean().sort_values()

    # Sort the x-axis values based on average values
    x_values = avg_values.index

    # Plot boxplot based on the column
    sns.boxplot(data=df_no_outliers, x=xcolumn, y=ycolumn, ax=ax, palette='viridis', order=x_values)
    ax.set_ylabel(ycolumn)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    ax.grid(False)


def generate_affordability_box_plot(df, xcolumn, ax):
    # Calculate affordability (Salary/Stipend - Required Income) grouped by field
    df['Affordability'] = df['Salary/Stipend'] - df['Required Income']

    df_no_outliers = remove_outliers(df, "Affordability")

    # Calculate average values for each x-value
    avg_values = df_no_outliers.groupby(xcolumn)["Affordability"].mean().sort_values()

    # Sort the x-axis values based on average values
    x_values = avg_values.index

    # Plot boxplot based on the column
    sns.boxplot(data=df_no_outliers, x=xcolumn, y="Affordability", ax=ax, palette='viridis', order=x_values)
    ax.set_ylabel("Affordability")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    ax.grid(False)