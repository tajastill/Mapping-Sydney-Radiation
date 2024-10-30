from ReadingFile import df
import geopandas as gpd
import pandas as pd
import folium
from folium import Choropleth
import json

# import a geojson file containing the postcode boundaries and add them to a dataframe. We use NSW for Sydney
postcodes = gpd.read_file('suburb-10-nsw.geojson')
df['geometry'] = gpd.points_from_xy(df['lon'], df['lat'])
df_gdf = gpd.GeoDataFrame(df, geometry='geometry', crs="EPSG:4326")
df_gdf.set_crs(epsg=4326, inplace=True)
postcodes = postcodes.to_crs(epsg=4326)
df = gpd.sjoin(df_gdf, postcodes, how='left', predicate='within')
df.to_csv('postcodes.csv')


# generate the mean Count Rate for each postcode
# group datapoints by postcode
postcode_means = df.groupby('nsw_loca_2')['countRate'].mean().reset_index()
postcodes = postcodes.merge(postcode_means, left_on='nsw_loca_2', right_on='nsw_loca_2', how='left')
for col in postcodes.select_dtypes(include=['datetime']).columns:
    postcodes[col] = postcodes[col].astype(str)


# initialise the folium map, centered at the center of the data
city_centre = [df['lat'].mean(), df['lon'].mean()]
m = folium.Map(location=city_centre, zoom_start=10)
folium.TileLayer('cartodbpositron').add_to(m)

geojson_data = json.loads(postcodes.to_json())

# plot datta as a chloropleth in folium
Choropleth(
    geo_data=postcodes,
    data=postcodes,
    columns=['nsw_loca_2', 'countRate'],
    key_on='feature.properties.nsw_loca_2',
    fill_color='YlOrRd',  # Color scale
    fill_opacity=0.4,
    line_opacity=0.2,
    legend_name='Mean countRate by Postcode'
).add_to(m)

# add labels for each suburb
folium.GeoJson(
    geojson_data,
    name='geojson',
    tooltip=folium.GeoJsonTooltip(
        fields=['nsw_loca_2', 'countRate'],
        aliases=['Suburb:', 'Mean CountRate:'],
        localize=True
    ),
    style_function=lambda feature: {
        'color': 'gray',
        'weight': 0.2,
        'fillOpacity': 0.1
    }
).add_to(m)


# individual HPGe data points
data = [
    [-33.847505, 151.230823, 4.14, 7.04, 5.02],
    [-33.887436, 151.187562, 0.52, 4.83, 1.69],
    [-33.904464, 151.2666819, 0.49, 4.02, 3.35],
    [-33.9082768, 151.2668111, 0.48, 4.30, 11.90],
    [-33.8917721, 151.2476105, 0.58, 6.56, 2.49],
    [-33.8738557, 151.2131167, 0.97, 6.30, 4.55],
    [-33.8768431, 151.2090893, 0.16, 4.09, 2.92],
    [-33.8837703, 151.194936, 0.43, 2.03, 0.52],
    [-33.8859338, 151.1901988, 0.11, 3.18, 2.23],
    [-33.8884707, 151.1890147, 4.71, 6.57, 3.80]
]


# plot the HPGe data on the map with pop-up text describing them
for lat, lon, k40, th232, u238 in data:
    popup_text = f"K40: {k40} mg/kg<br>Th: {th232} mg/kg<br>U: {u238} mg/kg"
    folium.Marker(
        location=[lat, lon],
        popup=popup_text,
        icon=folium.Icon(color="green", icon="info-sign")
    ).add_to(m)
print(df)
m.save("postcodes.html")
