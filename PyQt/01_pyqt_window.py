import sys
from PyQt5.QtWidgets import QApplication, QWidget

class WindowClass(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 300)
        self.setWindowTitle("Window - GeneticAlgorithmMario")
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WindowClass()
    window.show()
    app.exec_()
