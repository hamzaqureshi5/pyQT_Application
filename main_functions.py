from PyQt6.QtCore import QObject

debug=False

class MainClass(QObject):
    def __init__(self, de_tableWidget,de_comboBox, parent=None):
        super().__init__(parent)
        
        self.de_tableWidget = de_tableWidget
        self.de_comboBox=de_comboBox

        self.default_elect=""

