import sys
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
import numpy as np

class WindowClass(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 300)
        self.setWindowTitle("Window - GeneticAlgorithmMario")
        # Text
        label = QLabel(self)
        label.setGeometry(10, 10, 100, 10) # pos_x, pos_y, size_x, size_y(좌상단 0,0)
        label.setText("This is test text")
        # Img
        image = QLabel(self)
        image_array = np.array([[[255, 255, 255], [255, 255, 255]], [[255, 255, 255], [255, 255, 255]]])
        qimage = QImage(image_array, image_array.shape[1], image_array.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap(qimage)
        pixmap = pixmap.scaled(50, 50, Qt.IgnoreAspectRatio)
        image.setPixmap(pixmap)
        image.setGeometry(50, 50, 100, 100)
        #Button
        button = QPushButton(self)
        button.setText("Button")
        button.setGeometry(150, 150, 100, 50)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WindowClass()
    window.show()
    app.exec_()
