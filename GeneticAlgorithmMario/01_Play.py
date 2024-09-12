import retro
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
import numpy

class WindowClass(QWidget):
    def __init__(self):
        super().__init__()
        # Window init
        self.env = retro.make(game="SuperMarioBros-Nes", state="Level1-1")
        self.action = numpy.array([0, 0, 0, 0, 0, 0, 0, 0, 0])  # B,NULL,SELECT,START,U,D,L,R,A
        screen = self.env.reset()
        self.game_screen_width = screen.shape[0] * 2
        self.game_screen_height = screen.shape[1] * 2
        self.setFixedSize(self.game_screen_width, self.game_screen_height)
        self.setWindowTitle("Window - GeneticAlgorithmMario")
        # Game screen
        self.game_screen_label = QLabel(self)
        self.game_screen_label.setGeometry(0, 0, self.game_screen_width, self.game_screen_height)
        self.game_timer = QTimer(self)
        self.game_timer.timeout.connect(self.updateGameScreen)
        self.game_timer.start(1000 // 60) # 60hz
        # Show
        self.show()

    # Key event => [Up, Down, Left, Right, A, S]
    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Right:
            self.action[7] = 1
        elif key == Qt.Key_Left:
            self.action[6] = 1
        elif key == Qt.Key_Up:
            self.action[4] = 1
        elif key == Qt.Key_Down:
            self.action[5] = 1
        elif key == Qt.Key_S:
            self.action[8] = 1
        elif key == Qt.Key_A:
            self.action[0] = 1

    def keyReleaseEvent(self, event):
        key = event.key()
        if key == Qt.Key_Right:
            self.action[7] = 0
        elif key == Qt.Key_Left:
            self.action[6] = 0
        elif key == Qt.Key_Up:
            self.action[4] = 0
        elif key == Qt.Key_Down:
            self.action[5] = 0
        elif key == Qt.Key_S:
            self.action[8] = 0
        elif key == Qt.Key_A:
            self.action[0] = 0

    # Game screen update
    def updateGameScreen(self):
        # Action input
        self.env.step(self.action)
        # Draw screen
        screen = self.env.get_screen()
        screen = QPixmap(QImage(screen, screen.shape[1], screen.shape[0], QImage.Format_RGB888))
        screen = screen.scaled(self.game_screen_width, self.game_screen_height, Qt.IgnoreAspectRatio)
        self.game_screen_label.setPixmap(screen)
        # Update
        self.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WindowClass()
    window.show()
    app.exec_()