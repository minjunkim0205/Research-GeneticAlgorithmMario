import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QTimer

class WindowClass(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 300)
        self.setWindowTitle("Window - GeneticAlgorithmMario")
        # Timer
        self.qtimer = QTimer(self)
        self.qtimer.timeout.connect(self.timer)
        self.qtimer.start(1000)
        self.show()

    def timer(self):
        print("Enabled", end="\n")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WindowClass()
    window.show()
    app.exec_()


