from ntpath import join
import sys
import enum
from tkinter import Spinbox
import numpy as np
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Generate import generate
from Utilities import solve

class Operator(enum.Enum):
    Add = 0
    Subtract = 1
    Multiply = 2
    Divide = 3
    Constant = 4

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.domain = np.empty((0),np.int32)

class Cage:
    def __init__(self, operator, value, cells=[]):
        self.operator = operator
        self.value = value
        self.cells = cells

# cages = [Cage(operator=Operator.Divide, value=2, cells=[Cell(0,0), Cell(1,0)])
# , Cage(operator=Operator.Add, value=6, cells=[Cell(0,1), Cell(1,1),Cell(2,1)])
# , Cage(operator=Operator.Subtract, value=1, cells=[Cell(0,2), Cell(0,3)])
# , Cage(operator=Operator.Multiply, value=12, cells=[Cell(1,2), Cell(1,3), Cell(2,3)])
# , Cage(operator=Operator.Constant, value=1, cells=[Cell(2,0)])
# , Cage(operator=Operator.Add, value=5, cells=[Cell(3,2), Cell(2,2), Cell(3,3)])
# , Cage(operator=Operator.Subtract, value=1, cells=[Cell(3,0), Cell(3,1)])]

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Welcome to KenKen!'
        self.left = 10
        self.top = 10
        self.size = 4
        self.width = (self.size + 6)*40
        self.height = (self.size + 2)*40
        self.welcomeUI()

    def welcomeUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.welcome_label = QLabel("Welcome to", self)
        self.kenken_label = QLabel("KENKEN", self)

        QFontDatabase.addApplicationFont("PressStart2P-Regular.ttf")
        self.welcome_label.setFont(QFont('Press Start 2P', 10))
        self.kenken_label.setFont(QFont('Press Start 2P', 22))

        self.welcome_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.kenken_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.kenken_label.setAlignment(Qt.AlignCenter)

        self.welcome_label.resize(self.width-200, self.height-75)
        self.kenken_label.resize(self.width-200, self.height-75)

        self.welcome_label.move(40, 40)
        self.kenken_label.move(40, 80)

        self.welcome_label.setStyleSheet("border: solid gray; color: solid gray;"
                                    "border-width: 3px 3px 3px 3px;")
        self.kenken_label.setStyleSheet("color: red;")



        self.spinbox = QSpinBox(self)
        self.spinbox.resize(75, 25)
        self.spinbox.move(int(self.width/1.45), int(self.height/2.2))
        self.spinbox.setRange(3, 100)

        # Create generate button in the window
        button_start = QPushButton('Start', self)
        button_start.resize(75, 25)
        button_start.move(int(self.width/1.45),int(self.height/1.76))
        # connect button to function on_click
        button_start.clicked.connect(self.start_on_click)
        
        self.show()
    
    @pyqtSlot()
    def start_on_click(self):
        print("size: ", self.spinbox.text())
        self.cams = PuzzleWindow(int(self.spinbox.text())) 
        self.cams.show()
        self.close()

class PuzzleWindow(QDialog):
    def __init__(self, size, parent=None):
        super().__init__(parent)
        self.title = 'KenKen Puzzle!'
        self.left = 10
        self.top = 10
        self.size = size
        self.solved_board = np.empty((0, self.size), np.int32) 
        self.cages = []
        self.labels = []
        self.width = (self.size + 6)*40
        self.height = (self.size + 2)*40
        self.drawBoard()

    def drawBoard(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        # call generate function from generate.py
        self.cages,sol = generate(self.size)

        self.spinbox = QSpinBox(self)
        self.spinbox.resize(75, 25)
        self.spinbox.move(int(self.width-150), int(self.height/2.2))
        self.spinbox.setRange(3, 100)

        for i in range(self.size):
            for j in range(self.size):
                self.label = QLabel("", self)
                self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                self.label.setAlignment(Qt.AlignCenter)
        
                self.label.resize(40, 40)
                self.label.move((i+1)*40, (j+1)*40)
                self.label.setStyleSheet("border : solid black;"
                                            "border-width : 1px 1px 1px 1px;")

                self.labels.append(self.label)

        for cage in self.cages:
            if cage.operator == Operator.Constant:
                print(cage.value)
                self.label = self.labels[cage]
                self.label.setText("<sup>{}</sup>".format(cage.value))
                self.label.setStyleSheet("border : solid black;"
                                            "border-width : 2px 2px 2px 2px;")
            # else:
            #     self.label.setText("<sup>{}</sup>]".format(cage.operator, cage.value))
        
        
        # Create a button in the window
        self.button_generate = QPushButton('New Board', self)
        self.button_generate.resize(75, 25)
        self.button_generate.move(int(self.width-150),int(self.height/1.76))

        self.button_solve = QPushButton('Slove', self)
        self.button_solve.resize(75, 25)
        self.button_solve.move(int(self.width-150),int(self.height/1.47))

        self.button_reset = QPushButton('Reset', self)
        self.button_reset.resize(75, 25)
        self.button_reset.move(int(self.width-150),int(self.height/1.26))
        
        # connect button to function on_click
        self.button_generate.clicked.connect(self.generate_board)
        self.show()

        self.button_solve.clicked.connect(self.solve_board)
        self.show()

        self.button_reset.clicked.connect(self.reset_board)

    def generate_board(self):
        print("size: ", self.spinbox.text())
        self.cams = PuzzleWindow(int(self.spinbox.text())) 
        self.cams.show()
        self.close()
       
    
    def solve_board(self):
        solved = solve(self.cages, self.size, 0)
        self.solved_board = np.append(self.solved_board,solved)
        self.fill()

    def fill(self):
        for i in range(self.size * self.size):
            self.label = self.labels[i]
            self.label.setText("{}".format(self.solved_board[i]))


    def reset_board(self):
        for i in range(self.size * self.size):
            self.label = self.labels[i]
            self.label.setText(" ")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())