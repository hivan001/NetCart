from model import Model
from icon_group import IconGroup
from PySide6 import QtCore, QtWidgets, QtGui

class Controller():
    '''Controller class handles communication between model and view'''
    def __init__(self, model, view):
        self.path = "results/network_db.json"
        self.id_generator = 0
        self.model = model
        self.view = view
        self.data = self.get_model_data()
        # Arrays of QGraphicsItemGroups 
        self.pc_objects = []
        self.server_objects = []
        self.equipment_objects = []

        self.scene_coordinates = None
        self.view.cursor_signal.connect(self.update_scene_coordinates)
        self.view.add_pc_signal.connect(self.add_pc)
        self.view.add_server_signal.connect(self.add_server)
        self.view.add_router_signal.connect(self.add_router)
        self.view.add_switch_signal.connect(self.add_switch)


    
    def get_model_data(self):
        return self.model.read_db()
    
    def make_icon_group(self,icon,object_type):
        icon_group = IconGroup(icon,object_type)
        icon_group.remove_object_signal.connect(self.remove_object)
        return icon_group

    def make_pc_icon(self,pc_object):
        pixmap = self.view.icon.image_items[0].pixmap()
        pc_icon = QtWidgets.QGraphicsPixmapItem(pixmap)
        return self.make_icon_group(pc_icon,pc_object)
    
    def make_server_icon(self,server_object):
        pixmap = self.view.icon.image_items[1].pixmap()
        server_icon = QtWidgets.QGraphicsPixmapItem(pixmap)
        return self.make_icon_group(server_icon,server_object)
    

    def make_network_objects(self):
        for pc in self.data["resources"]["pcs"]:
            self.pc_objects.append(self.make_pc_icon(pc))

        for server in self.data["resources"]["servers"]:
            self.pc_objects.append(self.make_server_icon(server))

    def update_scene_coordinates(self,x,y):
        self.scene_coordinates = (x,y)

    def add_object_to_scene(self,object,x,y):
        object.setScale(0.25)
        object.setPos(x,y)
        object.setFlags(QtWidgets.QGraphicsPixmapItem.GraphicsItemFlag.ItemIsMovable | QtWidgets.QGraphicsPixmapItem.GraphicsItemFlag.ItemIsSelectable |
                        QtWidgets.QGraphicsPixmapItem.GraphicsItemFlag.ItemClipsToShape)
        self.view.scene.addItem(object)
        self.view.scene.update()        
    
    def add_pc(self):
        self.model.add_pc()
        self.data = self.get_model_data()
        # Most recent PC object should be the one we just made here
        pc = self.make_pc_icon(self.data["resources"]["pcs"][-1])
        self.pc_objects.append(pc)

        x = self.scene_coordinates[0]
        y = self.scene_coordinates[1]

        self.add_object_to_scene(pc,x,y)


    
    def add_server(self):
        self.model.add_server()
        self.data = self.get_model_data()
        server = self.make_server_icon(self.data["resources"]["servers"][-1])
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
        image_x = 10
        image_y = 50
        square_size = 200  # Adjust spacing between squares
        items_per_row = 3  # Number of items per row before wrapping
        row_count = 0      # Tracks the number of row changes

        all_objects = self.pc_objects + self.server_objects + self.equipment_objects

        for index, object in enumerate(all_objects):
            icon = object
            self.add_object_to_scene(icon,image_x,image_y)

            image_x += square_size  

        # Check if we should wrap to the next row
            if (index + 1) % items_per_row == 0:  
                image_x = 10  # Reset to starting x position
                image_y += square_size  # Move down a row
                row_count += 1  # Increase row count

