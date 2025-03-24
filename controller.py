from model import Model
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
    

    def make_icon_group(self,icon,object):
        icon_x_pos = icon.pos().x()
        icon_y_pos = icon.pos().y()
        icon_width = icon.pixmap().width()

        # Create a QWidget with a layout for the toggle button
        main_widget = QtWidgets.QWidget()
        main_layout = QtWidgets.QVBoxLayout(main_widget)

        main_widget.toggle_button = QtWidgets.QPushButton("IP: " + object["ip"])
        main_widget_font = QtGui.QFont("Arial", 50)
        main_widget.toggle_button.setFont(main_widget_font)
        main_widget.toggle_button.setCheckable(True)
        main_widget.toggle_button.setEnabled(True)
        main_widget.toggle_button.setChecked(False)
        main_widget.toggle_button.setStyleSheet(
            """QPushButton {
            border: 3px solid black;
            border-radius: 10px;
            padding: 5px;
            }
            """
        )
        main_widget.toggle_button.setFixedSize(800, 100)
        main_layout.addWidget(main_widget.toggle_button)

        # Proxy widget for the toggle button
        toggle_button = QtWidgets.QGraphicsProxyWidget()
        toggle_button.setWidget(main_widget)
        toggle_button.setPos(icon_x_pos + icon_width, icon_y_pos)


        # Create content area as a separate QWidget
        content_widget = QtWidgets.QWidget()
        content_layout = QtWidgets.QVBoxLayout(content_widget)
        content_widget.label = QtWidgets.QLabel("TCP Ports: ")

        # Looping through the ports and adding to the icon
        for port in object["tcp_ports"]:
            current_text = content_widget.label.text()
            content_widget.label.setText(current_text + "\n" + port + self.view.icon.get_service(port))


        content_font = QtGui.QFont("Arial", 40)
        content_widget.label.setFont(content_font)
        content_widget.label.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        content_widget.setFixedSize(800, 800)
        content_widget.setStyleSheet(
                        """QWidget {
            border: 3px solid black;
            border-radius: 10px;
            padding: 5px;
            }
            """
        )
        content_layout.addWidget(content_widget.label)

        # Proxy widget for the content area
        content_x_pos = toggle_button.pos().x()
        content_y_pos = toggle_button.pos().y() + 150
        content = QtWidgets.QGraphicsProxyWidget()
        content.setWidget(content_widget)
        content.setPos(content_x_pos, content_y_pos)  # Adjusted position

        # Group all items
        group = QtWidgets.QGraphicsItemGroup()
        group.addToGroup(icon)
        group.addToGroup(toggle_button)
        group.addToGroup(content)

        return group

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

