from icon import Icon
from PySide6 import QtCore, QtWidgets, QtGui

class MainView(QtWidgets.QGraphicsView):
    add_pc_signal = QtCore.Signal()
    add_server_signal = QtCore.Signal()
    add_router_signal = QtCore.Signal()
    add_switch_signal = QtCore.Signal()
    cursor_signal = QtCore.Signal(float,float)

    def __init__(self):
        super().__init__()

        # Setting up the Scene
        self.scene = QtWidgets.QGraphicsScene()
        self.setScene(self.scene)
        self.icon = Icon()

        # Sets Size of the scene
        self.setSceneRect(0,0,1200,700)

        # Setting up the legend
        legend = self.sceneRect()
        text_x_pos = legend.left() + 30
        text_y_pos = legend.bottom() - 50

        icon_left = legend.left()
        icon_bottom = legend.bottom() - 30
        

        legend_icons = self.icon.image_items
        legend_texts = ["- Client", "- Server"]


        #Adding the Icons
        for icon in legend_icons:
            icon.setScale(0.25)
            icon.setPos(icon_left,icon_bottom)
            self.scene.addItem(icon)
            icon_left+=90

        #Adding labels to the icons
        for legend_text in legend_texts:
            text = QtWidgets.QGraphicsSimpleTextItem()
            font = QtGui.QFont("Arial", 12, QtGui.QFont.Weight.Bold)
            text.setRotation(-45)
            text.setFont(font)
            text.setText(legend_text)
            text.setPos(text_x_pos - 10,text_y_pos+10)
            self.scene.addItem(text)
            text_x_pos+=98

        #Border Around the Legend
        legend_width = 400
        legend_height = 250
        legend_border = QtWidgets.QGraphicsRectItem(0,550,legend_width,legend_height)

        pen = QtGui.QPen(QtGui.QColor("black"))
        pen.setWidth(2)
        legend_border.setPen(pen)

        self.scene.addItem(legend_border)

        self.resize(1200,875)


    def contextMenuEvent(self, event: QtGui.QContextMenuEvent):
        """Override the right-click event to show a context menu."""

        menu = QtWidgets.QMenu(self)

        add_pc = QtGui.QAction("Add PC", self)
        add_server = QtGui.QAction("Add Server", self)
        add_router = QtGui.QAction("Add Router", self)
        add_switch = QtGui.QAction("Add Switch", self)

        # Need to send cursor coordinates to controller
        cursor_scene_pos = self.mapToScene(event.pos())  # Convert to scene coordinates
        self.cursor_signal.emit(cursor_scene_pos.x(), cursor_scene_pos.y())

        menu.addAction(add_pc)
        menu.addAction(add_server)
        menu.addAction(add_router)
        menu.addAction(add_switch)

        action = menu.exec(event.globalPos())  # Show menu at cursor position

        if action == add_pc:
            self.add_pc_signal.emit()
        elif action == add_server:
            self.add_server_signal.emit()
        elif action == add_router:
            self.add_router_signal.emit()
        elif action == add_switch:
            self.add_switch_signal.emit()
