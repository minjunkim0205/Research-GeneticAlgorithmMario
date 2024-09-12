import sys
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget

class WindowClass(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 300)
        self.setWindowTitle("Window - GeneticAlgorithmMario")
        self.show()
    # Key event
    def keyPressEvent(self, event):
        key = event.key()
        print(str(key), end="\n")
    def keyReleaseEvent(self, event):
        key = event.key()
        print(str(key), end="\n")
    # Draw event
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)

        painter.setPen(QPen(QColor.fromRgb(255, 0, 0), 2.0, Qt.SolidLine))
        painter.drawLine(0, 200, 400, 200)

        painter.setPen(QPen(QColor.fromRgb(0, 0, 0), 3.0, Qt.SolidLine))
        painter.setBrush(QBrush(QColor.fromRgb(0,255,0)))
        painter.drawRect(50, 50, 50, 50)

        painter.setPen(QPen(QColor.fromRgb(0, 0, 0), 1.0, Qt.SolidLine))
        painter.setBrush(QBrush(QColor.fromRgb(0,0,255)))
        painter.drawEllipse(100, 100, 50, 50)

        painter.setPen(QPen(QColor.fromRgb(0,0,0), 1.0, Qt.SolidLine))
        painter.setBrush(Qt.NoBrush)
        painter.drawText(300, 20, "This is test text")

        painter.end()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WindowClass()
    window.show()
    app.exec_()
