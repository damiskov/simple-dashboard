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
    datapath = f"{path}/price_{index}.csv"
    price_data = pd.read_csv(datapath)
    return price_data
    



def make_map():

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

    return