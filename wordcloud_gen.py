import matplotlib.pyplot as plt

import wordcloud
import os

from PIL import Image

from descartes import PolygonPatch
import shapefile
import geopandas
import numpy as np


# #Get shapefile as a 
# sf=shapefile.Reader(os.path.join(os.getcwd(),'LIST_ELECTORAL_DIVS_STATEWIDE'))
# sf = sf.__geo_interface__
# coastline_segments = sf['features']
# fig,ax = plt.subplots()
# for seg in coastline_segments[:100000]:
#     x,y = zip(*seg['geometry']["coordinates"])
#     ax.plot(x,y, color="k")
# plt.show()

if ("tasmania_mask.png" not in os.listdir()):
    gdf = geopandas.read_file("LIST_ELECTORAL_DIVS_STATEWIDE/list_electoral_divs_statewide.shp")
    exploded = gdf.explode(ignore_index=True)
    exploded = exploded[exploded.area > 1e+08]
    ax = exploded.plot(color = "k")
    ax.axis('off')
    fig = ax.get_figure()
    fig.set_figheight(6)
    fig.set_figwidth(6)
    fig.set_tight_layout(True)
    ax.relim()
    ax.autoscale()
    fig.set_dpi(800)
    fig.savefig("tasmania_mask.png", dpi = 800)

mask = np.array(Image.open("tasmania_mask.png"))
target_path = os.path.join(os.getcwd(), "words.txt")

with open(target_path, "r") as file:
    words = file.read()

wc = wordcloud.WordCloud(mode = "RGBA", background_color="black", mask = mask)
wc.generate_from_text(words)

array = wc.to_array()
fig,ax = plt.subplots(figsize = (6,6), tight_layout = True)
ax.axis('off')
ax.imshow(array)
fig.patch.set_facecolor("black")
print(array)
fig.savefig("wordcloud.png", dpi = 800)