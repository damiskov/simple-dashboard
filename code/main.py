import folium
from branca.colormap import linear
import pandas as pd
import json
# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
from pdf2image import convert_from_path
import glob


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
    

# def map_to_png(map_path):
#     # imgkit.from_file(f"{map_path}.html", f"{map_path}.png")
#     # Set up the Selenium WebDriver
#     # driver = webdriver.Chrome(ChromeDriverManager().install())
#     driver = webdriver.Chrome('/opt/homebrew/Caskroom/chromedriver/128.0.6613.84/chromedriver-mac-arm64/chromedriver')

#     # Load the HTML file
#     driver.get(f"{map_path}.html")

#     # Save the screenshot
#     driver.save_screenshot(f"{map_path}.png")

#     # Close the browser
#     driver.quit()
#     return None

def make_gif(indices, static_map_path):
    # List of image file names in the order you want them in the GIF
    print("Making gif")
    pdf_images = [static_map_path+f"_{i}.pdf" for i in indices]
    print(pdf_images)
    

    images = [convert_from_path(fname)[0] for fname in pdf_images]
    print("Successfully converted pdfs to PIL images")
    print(len(images))
    # # Open and append each image to the list
    # for filename in pdf_images:
    #     img = Image.open(filename)
    #     images.append(img)

    # Save the GIF
    images[0].save("gif/nordpool.gif", save_all=True, append_images=images[1:], duration=120, loop=0)
    return


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
    map_path = f'maps/nordpool_{index}'
    nordpool_map.save(f"{map_path}.html")
    # map_to_png(map_path)
    
    

    return None

def main():
    for i in range(1, 11):
        print(f"Saved map: {i}")
        make_and_save_map(i)
    make_gif([i for i in range(1,11)],"maps/static/nordpool")

if __name__=="__main__":
    main()