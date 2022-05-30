from ntpath import join
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
# from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QLabel, QSizePolicy
# from PyQt5.QtGui import QIcon
# from PyQt5.QtCore import pyqtSlot

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'KenKen Puzzle'
        self.left = 10
        self.top = 10
        self.size = 4
        self.width = (self.size + 6)*40
        self.height = (self.size + 2)*40
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.size = 4

        # Create textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(self.width/1.45, self.height/2.2)
        self.textbox.resize(100,25)

        for i in range(self.size):
            for j in range(self.size):
                self.label = QLabel("", self)
                self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                self.label.setAlignment(Qt.AlignCenter)
    
                # setting up the border with different size
                self.label.setStyleSheet("border : solid black;"
                                        "border-width : 1px 1px 1px 1px;")
                # for cage in cages:
                #     self.label.setText("<sup>{}</sup>]".format(cage.operator, cage.value))
        
                # resizing the label
                self.label.resize(40, 40)
        
                # moving the label
                self.label.move((i+1)*40, (j+1)*40)

        
        # Create a button in the window
        self.button = QPushButton('Generate', self)
        self.button.move(self.width/1.45,self.height/1.76)
        self.button = QPushButton('Slove', self)
        self.button.move(self.width/1.45,self.height/1.47)
        self.button = QPushButton('Clear', self)
        self.button.move(self.width/1.45,self.height/1.26)
        
        # connect button to function on_click
        self.button.clicked.connect(self.on_click)
        self.show()
    
    @pyqtSlot()
    def on_click(self):
        textboxValue = self.textbox.text()
        QMessageBox.question(self, 'Message - pythonspot.com', "You typed: " + textboxValue, QMessageBox.Ok, QMessageBox.Ok)
        self.textbox.setText("")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())