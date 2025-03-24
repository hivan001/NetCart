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

        #resizing images for standardization
image_paths = [pc_path, ad_path, db_path, web_path,server_path]

for image_path in image_paths:
    image = Image.open(image_path)
    width = 300
    height = 400
    resize = image.resize((width,height))
    resize.save(image_path)
