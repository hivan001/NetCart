from network_objects.icon import Icon
from PySide6 import QtCore, QtWidgets, QtGui

class MainView(QtWidgets.QGraphicsView):
    add_pc_signal = QtCore.Signal()
    add_server_signal = QtCore.Signal()
    add_router_signal = QtCore.Signal()
    add_switch_signal = QtCore.Signal()
    process_nmap_signal = QtCore.Signal()
    cursor_signal = QtCore.Signal(float,float)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("NetCart")
        self.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.SmoothPixmapTransform)
        self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.zoom_factor = 1.15  # how fast to zoom   

        # Setting up the Scene
        self.scene = QtWidgets.QGraphicsScene()
        self.setScene(self.scene)
        self.icon = Icon()

        # Get the users screen size
        screen = QtWidgets.QApplication.primaryScreen()
        screen_geometry = screen.geometry()

        # self.setFixedSize(screen_width, screen_height)
        self.setSceneRect(-999999, -999999, 1999999, 1999999)
        self.setInteractive(True)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setStyleSheet("background-color: #eaf4fb;")

        legend_origin_x = 0
        legend_origin_y = 720 - 150
        self.centerOn(legend_origin_x+750,legend_origin_y-200)
        
        icon_left = legend_origin_x
        icon_bottom = legend_origin_y + 35

        text_x_pos = legend_origin_x + 20
        text_y_pos = legend_origin_y

        legend_icons = self.icon.image_items
        legend_texts = ["- Workstation", "- Server"]


        #Adding the Icons
        for icon in legend_icons:
            icon.setScale(0.25)
            icon.setPos(icon_left,icon_bottom)
            self.scene.addItem(icon)
            icon_left+=95

        #Adding labels to the icons
        for legend_text in legend_texts:
            text = QtWidgets.QGraphicsSimpleTextItem()
            font = QtGui.QFont("Arial", 12, QtGui.QFont.Weight.Bold)
            text.setRotation(-45)
            text.setFont(font)
            text.setText(legend_text)
            text.setPos(text_x_pos,text_y_pos+10)
            self.scene.addItem(text)
            text_x_pos+=125

        #Border Around the Legend
        legend_width = 400
        legend_height = 150
        legend_border = QtWidgets.QGraphicsRectItem(legend_origin_x,legend_origin_y+25,legend_width,legend_height)

        pen = QtGui.QPen(QtGui.QColor("black"))
        pen.setWidth(1)
        legend_border.setPen(pen)

        self.scene.addItem(legend_border)

        # Create the nmap import gui

        self.input_overlay = QtWidgets.QWidget(self)
        self.input_overlay.setGeometry(0,0, 700, 500) 
        self.input_overlay.setStyleSheet("background-color: white; border: 1px solid gray;")
        self.input_overlay.hide()

        layout = QtWidgets.QVBoxLayout(self.input_overlay)
        self.import_nmap_label = QtWidgets.QLabel("Import Nmap Scan")
        font = QtGui.QFont("Arial", 12, QtGui.QFont.Weight.Bold)
        self.import_nmap_label.setFont(font)
        self.import_nmap_label.setAlignment(QtCore.Qt.AlignCenter)
        self.nmap_text_edit = QtWidgets.QTextEdit()
        self.submit_btn = QtWidgets.QPushButton("Submit")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

        btn_row = QtWidgets.QHBoxLayout()
        btn_row.addWidget(self.submit_btn)
        btn_row.addWidget(self.cancel_btn)
        layout.addWidget(self.import_nmap_label)
        layout.addWidget(self.nmap_text_edit)
        layout.addLayout(btn_row)

        # Cancel hides the overlay
        self.cancel_btn.clicked.connect(self.cancel_nmap_import)

        self.submit_btn.clicked.connect(self.process_nmap_signal.emit)

    def cancel_nmap_import(self):
        self.nmap_text_edit.clear()
        self.input_overlay.hide()

    def contextMenuEvent(self, event: QtGui.QContextMenuEvent):
        """Override the right-click event to show a context menu."""

        item = self.itemAt(event.pos())

        if isinstance(item, QtWidgets.QGraphicsProxyWidget):
            widget = item.widget()
            if isinstance(widget, QtWidgets.QLabel):
                super().contextMenuEvent(event)
                return

        menu = QtWidgets.QMenu(self)
        menu.setStyleSheet('''
                QMenu::item:selected {
                background-color: #4a90e2;
                color: white;
                }
                QMenu {
                background-color: #ffffff;
                border: 1px solid #ccc;
                }    
                ''')

        add_pc = QtGui.QAction("Add Workstation", self)
        add_server = QtGui.QAction("Add Server", self)
        # add_router = QtGui.QAction("Add Router", self)
        # add_switch = QtGui.QAction("Add Switch", self)

        # Need to send cursor coordinates to controller
        cursor_scene_pos = self.mapToScene(event.pos())  # Convert to scene coordinates
        self.cursor_signal.emit(cursor_scene_pos.x(), cursor_scene_pos.y())

        menu.addAction(add_pc)
        menu.addAction(add_server)
        # menu.addAction(add_router)
        # menu.addAction(add_switch)

        action = menu.exec(event.globalPos())  # Show menu at cursor position

        if action == add_pc:
            self.add_pc_signal.emit()
        elif action == add_server:
            self.add_server_signal.emit()
        # elif action == add_router:
        #     self.add_router_signal.emit()
        # elif action == add_switch:
        #     self.add_switch_signal.emit()


    def wheelEvent(self, event):
        if event.modifiers() == QtCore.Qt.ControlModifier:
            if event.angleDelta().y() > 0:
                zoom_factor = self.zoom_factor
            else:
                zoom_factor = 1 / self.zoom_factor

            self.scale(zoom_factor, zoom_factor)
        else:
            # Default scroll behavior (e.g., scroll the view normally)
            super().wheelEvent(event)
