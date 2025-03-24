import sys
import random
import copy
import icon
import json
from PIL import Image
from PySide6 import QtCore, QtWidgets, QtGui

class Results():
    ad_ports = ["88","464"]
    db_ports = ["3306","5432","27017","1521","1433"]
    web_ports = ["80","443","8080"]

    def __init__(self):
        self.icons = icon.Icon()
    

    def get_icon_type(self, ip):

        for port in ip["TCP Ports"]:
            if port in self.ad_ports:
                return self.icons.make_ad_icon(ip)
            elif port in self.db_ports:
                return self.icons.make_db_icon(ip)
            elif port in self.web_ports:
                return self.icons.make_web_icon(ip)
            else:
                return self.icons.make_pc_icon(ip)
            



    def get_results(self):
        json_path = "results/results.json"
        try:
            f = open(json_path,"r")
            json_data=json.load(f)
        except:
            print("Unable to open Results.json")

        return json_data


    def plot_results(self, scene):
        image_x = 10
        image_y = 50
        #Return icons in squares of 6
        square_count = 0

        data = self.get_results()

        for i in data["IPs"]:
            icon = self.get_icon_type(i)
            icon.setScale(0.25)
            icon.setPos(image_x,image_y)
            icon.setFlags(QtWidgets.QGraphicsPixmapItem.GraphicsItemFlag.ItemIsMovable | QtWidgets.QGraphicsPixmapItem.GraphicsItemFlag.ItemIsSelectable |
                            QtWidgets.QGraphicsPixmapItem.GraphicsItemFlag.ItemClipsToShape)
            scene.addItem(icon)
 
            if square_count == 0:  # Start new square
                image_x += 50
                square_count += 1
            elif square_count < 2:  # Continue horizontally
                image_x += 50
                square_count += 1
            elif square_count == 2:  # Drop down vertically
                image_y += 100
                square_count += 1
            elif square_count < 5:  # Move back horizontally
                image_x -= 50
                square_count += 1
            elif square_count == 5:  # Reset and move to new square group
                square_count = 0
                image_x += 200  # Move to the next grid's starting position
                image_y = 0  # Reset vertical position for the new square group
        
