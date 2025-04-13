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
image_paths = [pc_path, ad_path, db_path, web_path,server_path,icon_path]

for image_path in image_paths:
    if image_path != icon_path:
        width=300
        height= 400
    else:
        width = 64
        height = 64
        
    image = Image.open(image_path)
    width = 300
    height = 400
    resize = image.resize((width,height))
    resize.save(image_path)


