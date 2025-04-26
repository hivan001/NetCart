from model import Model
from network_objects.icon_group import IconGroup
from PySide6 import QtCore, QtWidgets, QtGui

class Controller():
    '''Controller class handles communication between model and view'''
    def __init__(self, model, view):
        self.id_generator = 0
        self.model = model
        self.path = self.model.get_db_path()
        self.view = view
        self.data = self.get_model_data()
        # Arrays of QGraphicsItemGroups 
        self.pc_objects = []
        self.server_objects = []
        self.equipment_objects = []

        self.scene_coordinates = (0,0)
        self.view.cursor_signal.connect(self.update_scene_coordinates)
        self.view.add_pc_signal.connect(self.add_pc)
        self.view.add_server_signal.connect(self.add_server)
        self.view.add_router_signal.connect(self.add_router)
        self.view.add_switch_signal.connect(self.add_switch)
        self.view.process_nmap_signal.connect(self.process_nmap_scan_objects)


    
    def get_model_data(self):
        return self.model.read_db()
    
    def make_icon_group(self,icon,object_type):
        icon_group = IconGroup(icon,object_type)
        icon_group.remove_object_signal.connect(self.remove_object)
        icon_group.ip_label.update_field_signal.connect(self.update_object)
        icon_group.tcp_text_edit.update_field_signal.connect(self.update_object)
        icon_group.udp_text_edit.update_field_signal.connect(self.update_object)
        return icon_group
    
    def update_object(self,object_id,field, field_data):
        self.model.update_field(object_id, field, field_data)

    def make_pc_icon(self,pc_object):
        pixmap = self.view.icon.image_items[0].pixmap()
        pc_icon = QtWidgets.QGraphicsPixmapItem(pixmap)
        return self.make_icon_group(pc_icon,pc_object)
    
    def make_server_icon(self,server_object):
        pixmap = self.view.icon.image_items[1].pixmap()
        server_icon = QtWidgets.QGraphicsPixmapItem(pixmap)
        return self.make_icon_group(server_icon,server_object)
    

    def make_network_objects(self):
        for index, db_object in enumerate(self.data["resources"]):
            for key,value in db_object.items():
                if key == "resource_type" and value == "workstation":
                    self.pc_objects.append(self.make_pc_icon(db_object))
                elif key == "resource_type" and value == "server":
                    self.pc_objects.append(self.make_server_icon(db_object))

    def update_scene_coordinates(self,x,y):
        print(x,y)
        self.scene_coordinates = (x,y)

    def add_object_to_scene(self,object,x,y):
        object.setScale(0.25)
        object.setPos(x,y)
        object.setFlags(QtWidgets.QGraphicsPixmapItem.GraphicsItemFlag.ItemIsMovable | QtWidgets.QGraphicsPixmapItem.GraphicsItemFlag.ItemIsSelectable |
                        QtWidgets.QGraphicsPixmapItem.GraphicsItemFlag.ItemClipsToShape)
        self.view.scene.addItem(object)
        self.view.scene.update()        
    
    def add_pc(self,ip="", tcp_ports="", udp_ports="", name="",x=0.0,y=0.0):

        # update the model
        self.model.add_pc(ip, tcp_ports,udp_ports,name)
        self.data = self.get_model_data()
        # Most recent PC object should be the one we just made here
        pc = self.make_pc_icon(self.data["resources"][-1])
        
        #update the gui
        pc.ip_label.setText(ip)        
        pc.tcp_text_edit.setText(tcp_ports)  
        pc.udp_text_edit.setText(udp_ports)


        self.pc_objects.append(pc)

        # get scene center coordinates
        # need to check if user is adding object via right click or via nmap scan import
        # if adding object via right click, the scene coordinates won't be (0,0)
        if self.scene_coordinates == (0,0):
            x = x
            y = y
        else:
            x = self.scene_coordinates[0]
            y = self.scene_coordinates[1]


        self.add_object_to_scene(pc,x,y)


    
    def add_server(self):
        self.model.add_server()
        self.data = self.get_model_data()
        server = self.make_server_icon(self.data["resources"][-1])
        self.server_objects.append(server)

        x = self.scene_coordinates[0]
        y = self.scene_coordinates[1]

        self.add_object_to_scene(server,x,y)

    def remove_object(self,object_id,resource_object):
        self.model.remove_resource(object_id)
        self.view.scene.removeItem(resource_object)

    def add_router(self):
        print("router")

    def add_switch(self):
        print("switch")    

    # type = pcs or servers
    def plot_results(self):
        self.make_network_objects()
        image_x = 0
        image_y = 0
        square_count = 0

        all_objects = self.pc_objects + self.server_objects + self.equipment_objects

        for index, object in enumerate(all_objects):
            icon = object
            self.add_object_to_scene(icon,image_x,image_y)

            if square_count == 0:  # Start new square
                image_x += 200
                square_count += 1
            elif square_count < 2:  # Continue horizontally
                image_x += 200
                square_count += 1
            elif square_count == 2:  # Drop down vertically
                image_y += 300
                square_count += 1
            elif square_count < 5:  # Move back horizontally
                image_x -= 200
                square_count += 1
            elif square_count == 5:  # Reset and move to new square group
                square_count = 0
                image_x += 600  # Move to the next grid's starting position
                image_y = 0  # Reset vertical position for the new square group


    def process_nmap_scan_objects(self):
        text = self.view.nmap_text_edit.toPlainText()
        objects = self.model.process_nmap_scan(text)
        x = 635.0
        y = 360.0

        for key,object in objects.items():
            # we'll make all objects pcs for now, up to user to change to server
            self.add_pc(ip=key,tcp_ports=object[0]["tcp_ports"],udp_ports=object[0]["udp_ports"],x=x, y=y)
            x+=200.0
