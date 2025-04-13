import sys
from main_view import MainView
from model import Model
from controller import Controller
from PySide6 import QtWidgets,QtGui

def main():
    app = QtWidgets.QApplication([])
    app.setWindowIcon(QtGui.QIcon("/static/net_cart_icon.png"))
    main_view = MainView()
    model = Model()
    controller = Controller(model=model, view=main_view)

    # This is the initial read of the JSON
    controller.plot_results()  

    main_view.show()
    sys.exit(app.exec())    



if __name__ == "__main__":
    main()
