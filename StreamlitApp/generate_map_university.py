import plotly.express as px

def generate_map2(df, criteria):
    # Define a colormap based on the criteria values
    values = df[criteria].sort_values()
    colorblind_friendly_colors = ['#4A90E2', '#50E3C2', '#F5A623', '#D0021B', '#9013FE']

    # Remove duplicates based on location and study_name
    df = df.drop_duplicates(subset=['LATITUDE', 'LONGITUDE', 'University'])

    # Format criteria text
    criteria_text = ' '.join(word.capitalize() for word in criteria.split('_'))

    # Create a map object using Plotly Express
    fig = px.scatter_geo(
        df,
        lat="LATITUDE",
        lon="LONGITUDE",
        hover_name="University",
        size=criteria,
        color=criteria,
        color_continuous_scale=colorblind_friendly_colors,
        range_color=(values.min(), values.max()),
        projection="natural earth",
        title=f"Schools by {criteria_text}",
        text="University",
        custom_data=[criteria],
    )

    # Customize hover information
    fig.update_traces(
        hovertemplate="<b>%{hovertext}</b><br>{criteria_text}: %{customdata[0]}"
    )
    
    fig.update_geos(
        center=dict(lat=30, lon=-95), # Center the map at the specified coordinates
        projection_scale=3.5 # Set the zoom level
    )


    # Return the map object
    return fig