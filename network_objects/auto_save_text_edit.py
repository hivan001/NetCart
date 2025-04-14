from PySide6 import QtWidgets, QtCore, QtGui

class AutoSaveTextEdit(QtWidgets.QTextEdit):
    update_field_signal = QtCore.Signal(int, str,str)
    def __init__(self,object_id, field_name, parent=None):
        super().__init__(parent)
        self.field_name = field_name
        self.object_id = object_id
    
    def focusOutEvent(self, event):
        self.update_field_signal.emit(self.object_id,self.field_name,self.toPlainText())
        super().focusOutEvent(event)
