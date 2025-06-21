# map_utils.py
# Utility functions for integrating maps (free APIs)

import folium

def generate_map(locations, output_file="map.html"):
    # `locations` is a list of dicts with 'name', 'lat', 'lon'
    if not locations:
        return None

    map_center = [locations[0]['lat'], locations[0]['lon']]
    m = folium.Map(location=map_center, zoom_start=6)

    for loc in locations:
        folium.Marker(
            location=[loc['lat'], loc['lon']],
            popup=loc['name'],
            icon=folium.Icon(color='blue')
        ).add_to(m)

    m.save(output_file)
    return output_file
