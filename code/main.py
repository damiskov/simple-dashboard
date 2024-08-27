print("Hello")
import folium
import geopandas as gpd
import geodatasets 
from branca.colormap import linear
import pandas as pd
import requests 
import json
import random

# globals


cph = [55.6761,12.5683] 
ber = [52.52, 13.41]
lon = [51.5, -0.128]
vie = [48.2, 16.4]
sto = [59.3, 18.1]
osl = [59.9, 10.8]

nordpool_members = ["Ireland", "United Kingdom", "France", "Belgium", "Netherlands",
                    "Germany", "Austria", "Poland", "Latvia", "Estonia", "Lithuania",
                    "Denmark", "Norway", "Sweden", "Finland", "Luxembourg"]

def load_geojson(path='data/europe.geojson'):
    with open(path, 'r') as f:
        europe = json.load(f)
        return europe
    

def load_price(index, path='data/pricing/'):
    datapath = f"{path}/electricity_prices_{index}.csv"
    price_data = pd.read_csv(datapath)
    return price_data
    



def make_and_save_map(index):

    price_data = load_price(index)

    map_size = 20 # Determine size of map around cph (Doesn't appear to change anything in notebook.)
    min_lon, max_lon = cph[0]-map_size, cph[0]+map_size
    min_lat, max_lat = cph[1]-map_size, cph[0]+map_size
    nordpool_map = folium.Map(location=cph,
                            zoom_start=5,
                            min_lat=min_lat,
                            max_lat=max_lat,
                            min_lon=min_lon,
                            max_lon=max_lon,
                            zoom_control=False)
    colormap = linear.YlGn_09.scale(
    -10, 210)
    eu_geojson = load_geojson()

    folium.Choropleth(
    geo_data=eu_geojson,
    data = price_data,
    columns=['Country', 'Price'],
    key_on= 'feature.properties.NAME',
    fill_color="YlGn",
    fill_opacity=0.7,
    line_opacity=0.2,
    highlight=True,
    legend_name="Price (€/MWh)"
    ).add_to(nordpool_map)

    folium.LayerControl().add_to(nordpool_map)

    # saving
    nordpool_map.save(f'maps/interactive/nordpool_{index}.html')
    return None

def main():
    for i in range(1, 11):
        make_and_save_map(i)


if __name__=="__main__":
    main()