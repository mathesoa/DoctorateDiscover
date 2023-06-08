
import plotly.express as px

def generate_map(df):
    # Define a colormap based on the rank values
    ranks = df['rank']
    colorblind_friendly_colors = ['#4A90E2', '#50E3C2', '#F5A623', '#D0021B', '#9013FE']


    # Create a map object using Plotly Express
    fig = px.scatter_geo(
        df,
        lat="Latitude",
        lon="Longitude",
        hover_name="name",
        color="rank",
        color_continuous_scale=colorblind_friendly_colors,
        range_color=(ranks.min(), ranks.max()),
        projection="natural earth",
        #title="University Locations by World Rank",
    )
    
    fig.update_geos(
        center=dict(lat=20, lon=-20), # Center the map at the specified coordinates
        projection_scale=2 # Set the zoom level
    )
    fig.update_traces(marker=dict(sizemin=40))
    
    fig.update_layout(
    autosize=False,
    width=650,
    height=400,
    )
    
    # Return the map object
    return fig
