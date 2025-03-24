import sys
import random
import os
import copy
from PIL import Image
from PySide6 import QtCore, QtWidgets, QtGui

class Icon(QtWidgets.QGraphicsView):
    image_items = []
    services = {
        "20":"FTP-DATA","21":"FTP","22":"SSH","23":"TELNET","25":"SMTP","53":"DNS",
        "69":"TFTP","80":"HTTP","88":"KERBEROS","110":"POP3","143":"IMAP","443":"HTTPS",
        "445":"SMB","464":"KERBEROS-PASS","587":"SMTP","636":"LDAP-SSL","3306":"MYSQL",
        "5432":"POSTGRESQL","3389":"RDP","27017":"MONGODB","1521":"ORACLEDB","1433":"MSSQL",
        "8080":"HTTP-PROXY"
    }
    def __init__(self):
        super().__init__()

        pc_path = "static/pc.png"
        server_path = "static/server.png"

        pc_pixmap = QtGui.QPixmap(pc_path)
        server_pixmap = QtGui.QPixmap(server_path)

        pc_image_item = QtWidgets.QGraphicsPixmapItem(pc_pixmap)
        server_image_item = QtWidgets.QGraphicsPixmapItem(server_pixmap)

        self.image_items.append(pc_image_item)
        self.image_items.append(server_image_item)
        
    def get_service(self, port):
        if port in self.services:
            return f" - {self.services[port]}"
        else:
            return ""





        

    