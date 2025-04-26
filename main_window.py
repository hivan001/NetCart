from PySide6 import QtWidgets, QtGui, QtCore
from main_view import MainView

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NetCart")

        self.view = MainView()
        self.setCentralWidget(self.view)

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        import_menu = menu_bar.addMenu("Import")

        new_map = QtGui.QAction("New Map", self)
        open_map = QtGui.QAction("Open Map", self)
        exit_action = QtGui.QAction("Exit", self)
        import_action = QtGui.QAction("Import Nmap Scan", self)

        exit_action.triggered.connect(self.close)

        file_menu.addAction(new_map)
        file_menu.addAction(open_map)
        file_menu.addAction(exit_action)

        import_menu.addAction(import_action)

        menu_bar.setStyleSheet("border: 1px solid gray; border-radius: 8px; padding 10px;")

        import_action.triggered.connect(self.view.input_overlay.show)


        screen = QtWidgets.QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        screen_width = screen_geometry.width() * .80
        screen_height = screen_geometry.height() * .80

        self.setFixedSize(screen_width, screen_height)

        # self.resize(screen_width, screen_height)
        self.center()

    def center(self):
        frameGm = self.frameGeometry()
        screen = self.screen().availableGeometry().center()
        frameGm.moveCenter(screen)
        self.move(frameGm.topLeft())


