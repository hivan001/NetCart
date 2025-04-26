from PySide6 import QtWidgets, QtCore, QtGui
from network_objects.auto_save_text_edit import AutoSaveTextEdit
class IconGroup(QtWidgets.QGraphicsWidget):
    remove_object_signal = QtCore.Signal(int, object)

    def __init__(self, icon, object_type):
        super().__init__()
        self.setData(0, object_type["id"])

        self.ip_label = AutoSaveTextEdit(self.data(0), "ip")
        self.tcp_text_edit = AutoSaveTextEdit(self.data(0), "tcp_ports")
        self.udp_text_edit = AutoSaveTextEdit(self.data(0), "udp_ports")

        self.setFlags(
            QtWidgets.QGraphicsItem.ItemIsMovable |
            QtWidgets.QGraphicsItem.ItemIsFocusable |
            QtWidgets.QGraphicsItem.ItemSendsGeometryChanges
        )

        # Styles
        label_style = "border: 2px solid black; border-radius: 12px; padding 10px;background-color:lightgray;"
        button_style = '''
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

        # Layout setup
        layout = QtWidgets.QGraphicsLinearLayout(QtCore.Qt.Orientation.Vertical)
        self.setLayout(layout)

        # Icon setup
        icon_label = QtWidgets.QLabel()
        icon_label.setPixmap(icon.pixmap())
        icon_label.setFixedWidth(500)
        layout.addItem(self._create_proxy(icon_label))

        # IP label setup
        self.ip_label.setPlainText(f"{object_type['ip']}")
        self.ip_label.setFont(QtGui.QFont("Arial", 40))
        self.ip_label.setStyleSheet(label_style)
        self.ip_label.setFixedSize(500, 75)
        self.ip_label.setReadOnly(False)
        layout.addItem(self._create_proxy(self.ip_label))

        # TCP Button first
        tcp_button = QtWidgets.QPushButton("TCP Ports:")
        tcp_button.setCheckable(True)
        tcp_button.setChecked(True)
        tcp_button.setStyleSheet(button_style)
        tcp_button.setFixedSize(500, 75)
        tcp_button.setFont(QtGui.QFont("Arial", 30, QtGui.QFont.Bold))
        layout.addItem(self._create_proxy(tcp_button))

        # TCP TextEdit after
        self.tcp_text_edit.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.tcp_text_edit.setFont(QtGui.QFont("Arial", 30))
        self.tcp_text_edit.setStyleSheet(label_style)
        self.tcp_text_edit.setFixedSize(500, 200)
        self.tcp_text_edit.setReadOnly(False)
        self.tcp_text_edit.setPlainText(object_type["tcp_ports"].strip())
        layout.addItem(self._create_proxy(self.tcp_text_edit))

        # Link button and text edit visibility
        tcp_button.toggled.connect(self.tcp_text_edit.setVisible)

        # UDP Button first
        udp_button = QtWidgets.QPushButton("UDP Ports:")
        udp_button.setCheckable(True)
        udp_button.setChecked(True)
        udp_button.setStyleSheet(button_style)
        udp_button.setFixedSize(500, 75)
        udp_button.setFont(QtGui.QFont("Arial", 30, QtGui.QFont.Bold))
        layout.addItem(self._create_proxy(udp_button))

        # UDP TextEdit after
        self.udp_text_edit.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.udp_text_edit.setFont(QtGui.QFont("Arial", 30))
        self.udp_text_edit.setStyleSheet(label_style)
        self.udp_text_edit.setFixedSize(500, 200)
        self.udp_text_edit.setReadOnly(False)
        self.udp_text_edit.setPlainText(object_type["udp_ports"].strip())
        layout.addItem(self._create_proxy(self.udp_text_edit))

        # Link button and text edit visibility
        udp_button.toggled.connect(self.udp_text_edit.setVisible)

        self.setMinimumSize(850, 750)

    def _create_proxy(self, widget):
        proxy = QtWidgets.QGraphicsProxyWidget()
        proxy.setWidget(widget)
        return proxy

    def update_field(self, controller, field):
        controller.model.update_field(field)

    def contextMenuEvent(self, event):
        """Override the right-click event to remove object."""
        menu = QtWidgets.QMenu(parent=self)
        remove_object = QtGui.QAction("Remove From Map", self)
        menu.addAction(remove_object)

        action = menu.exec(event.screenPos())  # Show menu at cursor position

        if action == remove_object:
            self.remove_object_signal.emit(self.data(0), self)
