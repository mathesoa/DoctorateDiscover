import folium
from branca.colormap import LinearColormap



def world_rank_map(df):
    # Define a colormap based on the rank values
    ranks = df['rank']
    cmap = LinearColormap(['green', 'yellow', 'red'], vmin=ranks.min(), vmax=ranks.max())

    # Create a map object
    m = folium.Map(location=[20, -20], zoom_start=2)

    # Add markers for each school to the map
    for i, row in df.iterrows():
        rank = row['rank']
        location = (row['Latitude'], row['Longitude'])
        popup_text = f"{rank}"
        
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
    cmap = LinearColormap(['green', 'yellow', 'red'], vmin=values.min(), vmax=values.max())

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
        
        # Add a custom HTML marker to the map
        html = f'<div style="font-size: 10pt; color: black;">{popup_text}</div>'
        marker = folium.map.Marker(location=location, icon=folium.DivIcon(html=html))
        marker.add_to(m)

    # Add the colormap to the map
    cmap.caption = 'School Rank'
    cmap.add_to(m)

    # Return the map object
    return m