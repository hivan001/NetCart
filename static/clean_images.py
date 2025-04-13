import sys
import os
import copy
from PIL import Image

# This script is to resize any new static image assets added to the app

pc_path = "static/pc.png"
ad_path = "static/ad.png"
db_path = "static/db.png"
web_path = "static/web.png"
server_path = "static/server.png"
icon_path = "static/net_cart_icon.png"

        #resizing images for standardization
image_paths = [pc_path, ad_path, db_path, web_path,server_path]

for image_path in image_paths:
    width=300
    height= 400 
    image = Image.open(image_path)
    resize = image.resize((width,height))
    resize.save(image_path)


image = Image.open(icon_path)
resize = image.resize((65,65))
resize.save(icon_path)

