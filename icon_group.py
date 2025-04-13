from PySide6 import QtWidgets, QtCore, QtGui
from auto_save_text_edit import AutoSaveTextEdit
class IconGroup(QtWidgets.QGraphicsWidget):
    remove_object_signal = QtCore.Signal(int,object)
    def __init__(self,icon, object_type):
        super().__init__()
        self.setData(0,object_type["id"])
        self.ip_label = AutoSaveTextEdit(self.data(0),"ip")
        self.tcp_text_edit = AutoSaveTextEdit(self.data(0),"tcp_ports")
        self.udp_text_edit = AutoSaveTextEdit(self.data(0),"udp_ports")
        self.setFlags(
            QtWidgets.QGraphicsItem.ItemIsMovable |
            QtWidgets.QGraphicsItem.ItemIsFocusable |
            QtWidgets.QGraphicsItem.ItemSendsGeometryChanges
        )
        
        label_style = "border: 2px solid black; border-radius: 12px; padding 10px;background-color:lightgray ;"
        button_style ='''
            QPushButton {
        border: 2px solid black;
        border-radius: 10px;
        background-color: lightgray;
        padding: 10px;
        }

        QPushButton:hover {
            background-color: green;
        }

        QPushButton:pressed {
            background-color: #cccccc;
        }
        '''


        layout = QtWidgets.QGraphicsLinearLayout(QtCore.Qt.Orientation.Vertical)
        self.setLayout(layout)

        icon_label = QtWidgets.QLabel()
        icon_label.setPixmap(icon.pixmap())
        icon_label.setFixedWidth(500)  


        self.ip_label.setPlainText(f"{object_type['ip']}")
        self.ip_label.setFont(QtGui.QFont("Arial", 40))
        self.ip_label.setStyleSheet(label_style)
        self.ip_label.setFixedSize(500, 75)
        self.ip_label.setReadOnly(False)

        # tcp_text_edit = QtWidgets.QTextEdit()
        self.tcp_text_edit.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.tcp_text_edit.setVisible(True)
        self.tcp_text_edit.setFont(QtGui.QFont("Arial", 30))
        self.tcp_text_edit.setStyleSheet(label_style)
        self.tcp_text_edit.setFixedSize(500, 200)
        self.tcp_text_edit.setReadOnly(False)

        tcp_button = QtWidgets.QPushButton("TCP Ports:")
        tcp_button.setCheckable(True)
        tcp_button.setChecked(True)
        tcp_button.toggled.connect(self.tcp_text_edit.setVisible)
        tcp_button.setStyleSheet(button_style)
        tcp_button.setFixedSize(500,75)
        tcp_button.setFont(QtGui.QFont("Arial", 30, QtGui.QFont.Bold))
        content_text=object_type["tcp_ports"]
        # for port in object_type["tcp_ports"]:
        #     content_text += f"{port}\n"

        self.tcp_text_edit.setPlainText(content_text.strip())



        # udp_text_edit = QtWidgets.QTextEdit()
        self.udp_text_edit.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.udp_text_edit.setVisible(True)
        self.udp_text_edit.setFont(QtGui.QFont("Arial", 30))
        self.udp_text_edit.setStyleSheet(label_style)
        self.udp_text_edit.setFixedSize(500, 200)
        self.udp_text_edit.setReadOnly(False)

        udp_button = QtWidgets.QPushButton("UDP Ports:")
        udp_button.setCheckable(True)
        udp_button.setChecked(True)
        udp_button.toggled.connect(self.udp_text_edit.setVisible)
        udp_button.setStyleSheet(button_style)
        udp_button.setFixedSize(500,75)
        udp_button.setFont(QtGui.QFont("Arial", 30, QtGui.QFont.Bold))
        content_text=object_type["udp_ports"]
        # for port in object_type["udp_ports"]:
        #     content_text += f"{port}\n"

        self.udp_text_edit.setPlainText(content_text.strip())


        icon_proxy = QtWidgets.QGraphicsProxyWidget()
        icon_proxy.setWidget(icon_label)
        layout.addItem(icon_proxy)

        ip_label_proxy = QtWidgets.QGraphicsProxyWidget()
        ip_label_proxy.setWidget(self.ip_label)
        layout.addItem(ip_label_proxy)

        tcp_button_proxy = QtWidgets.QGraphicsProxyWidget()
        tcp_button_proxy.setWidget(tcp_button)
        layout.addItem(tcp_button_proxy)

        tcp_text_proxy = QtWidgets.QGraphicsProxyWidget()
        tcp_text_proxy.setWidget(self.tcp_text_edit)
        layout.addItem(tcp_text_proxy)

        udp_button_proxy = QtWidgets.QGraphicsProxyWidget()
        udp_button_proxy.setWidget(udp_button)
        layout.addItem(udp_button_proxy)

        udp_text_proxy = QtWidgets.QGraphicsProxyWidget()
        udp_text_proxy.setWidget(self.udp_text_edit)
        layout.addItem(udp_text_proxy)

        self.setMinimumSize(850, 750)


    def update_field(self, controller,field):
        controller.model.update_field(field)


    def contextMenuEvent(self, event):
        """Override the right-click event to be able to remove object."""

        menu = QtWidgets.QMenu()
        remove_object = QtGui.QAction("Remove From Map", self)
        menu.addAction(remove_object)

        action = menu.exec(event.screenPos())  # Show menu at cursor position

        if action == remove_object:
            self.remove_object_signal.emit(self.data(0),self)