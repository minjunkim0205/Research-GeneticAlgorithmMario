import retro
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QBrush, QColor
import numpy
import tensorflow

class WindowClass(QWidget):
    def __init__(self):
        super().__init__()
        # Window init
        self.env = retro.make(game="SuperMarioBros-Nes", state="Level1-1")
        self.action = numpy.array([0, 0, 0, 0, 0, 0, 0, 0, 0])  # B,NULL,SELECT,START,U,D,L,R,A
        screen = self.env.reset()
        self.game_screen_width = screen.shape[0] * 2
        self.game_screen_height = screen.shape[1] * 2
        self.setFixedSize(self.game_screen_width+320, self.game_screen_height)
        self.setWindowTitle("Window - GeneticAlgorithmMario")
        # Game screen
        self.game_screen_label = QLabel(self)
        self.game_screen_label.setGeometry(0, 0, self.game_screen_width, self.game_screen_height)
        self.game_timer = QTimer(self)
        self.game_timer.timeout.connect(self.updateGameScreen)
        self.game_timer.start(1000 // 60) # 60hz
        # Tensorflow init
        self.model = tensorflow.keras.Sequential([
            tensorflow.keras.layers.Dense(9, input_shape=(8 * 10,), activation="relu"),
            tensorflow.keras.layers.Dense(6, activation="sigmoid")
        ])
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
    
    def paintEvent(self, event):
        # Painter init
        painter = QPainter()
        painter.begin(self)
        painter.setPen(QPen(Qt.black))
        # Get ram
        ram = self.env.get_ram()
        
        tiles = ram[0x0500:0x069F+1] # 0x0500-0x069F	Current tile (Does not effect graphics)
        tile_count = tiles.shape[0]
        tiles_current = tiles[:tile_count//2].reshape((13, 16))
        tiles_next = tiles[tile_count//2:].reshape((13, 16))
        tiles = numpy.concatenate((tiles_current, tiles_next), axis=1).astype(numpy.int32)

        enemy_drawn = ram[0x000F:0x0013+1] # 0x000F-0x0013	Enemy drawn? Max 5 enemies at once. => 0:No,1:Yes (not so much drawn as "active" or something)

        enemy_horizon = ram[0x006E:0x0072+1] # 0x006E-0x0072	Enemy horizontal position in level
        enemy_screen_x = ram[0x0087:0x008B+1] # 0x0087-0x008B	Enemy x position on screen
        enemy_y = ram[0x00CF:0x00D3+1] # 0x00CF-0x00D3	Enemy y pos on screen
        enemy_x = (enemy_screen_x + (enemy_horizon * 256)) % 512

        enemy_tile_x = (enemy_x + 8) // 16
        enemy_tile_y = (enemy_y - 8) // 16 - 1
        # Merge tiles
        for index, enemy in enumerate(enemy_drawn):
            if enemy == 1:
                if 0 <= enemy_tile_x[index] < tiles.shape[1] and 0 <= enemy_tile_y[index] < tiles.shape[0]:
                    tiles[enemy_tile_y[index]][enemy_tile_x[index]] = -1

        current_screen_page = ram[0x071A] # 0x071A	Current screen (in level)
        screen_position = ram[0x071C] # 0x071C	ScreenEdge X-Position, loads next screen when player past it?
        screen_offset = (256 * current_screen_page + screen_position) % 512
        screen_tile_offset = screen_offset // 16
        tiles = numpy.concatenate((tiles, tiles), axis=1)[:, screen_tile_offset:screen_tile_offset+16]

        for i in range(tiles.shape[0]):
            for j in range(tiles.shape[1]):
                if tiles[i][j] > 0:
                    tiles[i][j] = 1
                    painter.setBrush(QBrush(Qt.cyan))
                elif tiles[i][j] == -1:
                    tiles[i][j] = 2
                    painter.setBrush(QBrush(Qt.red))
                else:
                    painter.setBrush(QBrush(Qt.gray))
                painter.drawRect(self.game_screen_width + 20 * j, 20 * i, 20, 20)

        player_x = ram[0x03AD] # 0x03AD	Player x pos within current screen offset
        player_y = ram[0x03B8] # 0x03B8	Player y pos within current screen
        # Convert screen coordinates to tile coordinates
        player_tile_x = (player_x + 8) // 16
        player_tile_y = (player_y + 8) // 16 - 1

        painter.setBrush(QBrush(Qt.blue))
        painter.drawRect(self.game_screen_width + 20 * player_tile_x, 20 * player_tile_y, 20, 20)

        painter.setPen(QPen(Qt.magenta, 4, Qt.SolidLine))
        painter.setBrush(Qt.NoBrush)

        frame_x = player_tile_x
        frame_y = 2
        painter.drawRect(self.game_screen_width + 20 * frame_x, 20 * frame_y, 20 * 8, 20 * 10)
        input_data = tiles[frame_y:frame_y+10, frame_x:frame_x+8]

        if 2 <= player_tile_y <= 11:
            input_data[player_tile_y - 2][0] = 2
            
        input_data = input_data.flatten() # Reinforcement learning input
        # Reinforcement learning
        #print(input_data, end="\n")
        predict = self.model.predict(numpy.array([input_data]))[0]
        output_data = (predict > 0.5).astype(numpy.int32)
        print(output_data, end="\n")
        # Key output
        for index, key in enumerate(self.action):
            if key == 1:
                painter.setBrush(QBrush(Qt.magenta))
            else:
                painter.setBrush(QBrush(Qt.gray))
            painter.drawEllipse(self.game_screen_width + 10 + index * 35, 455, 10 * 2, 10 * 2)
            text = ("B", " ", " ", " ", "U", "D", "L", "R", "A")[index]
            painter.drawText(self.game_screen_width + 10 + index * 35, 455, text)
        # Painter end
        painter.end()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WindowClass()
    window.show()
    app.exec_()