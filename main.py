import sys
# from main_view import MainView
from main_window import MainWindow
from model import Model
from controller import Controller
from PySide6 import QtWidgets,QtGui

def main():
    app = QtWidgets.QApplication([])
    app.setWindowIcon(QtGui.QIcon("/static/net_cart_icon.png"))
    main_window = MainWindow()
    model = Model()
    controller = Controller(model=model, view=main_window.view)
    # This is the initial read of the JSON
    controller.plot_results()  

    main_window.show()
    sys.exit(app.exec())    



if __name__ == "__main__":
    main()
