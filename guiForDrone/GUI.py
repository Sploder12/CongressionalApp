import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QWidget, QToolTip,
    QPushButton, QApplication, QProgressBar, QSlider, QLCDNumber)
from PyQt5.QtGui import QFont


class Example(QWidget):

    def anyName(self, name):
        #put code here and will run after corresponding button is clicked
        def printName():
            print(name)
        return printName

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tello Drone GUI")
        self.setFixedWidth(1026)
        self.setFixedHeight(584)

        self.initUI()


    def initUI(self):

        QToolTip.setFont(QFont('SansSerif', 10))

        self.setToolTip('This is a <b>QWidget</b> widget')

        #forward
        forwardBtn = QPushButton('Forward', self)
        forwardBtn.setGeometry(QtCore.QRect(130, 337, 93, 51))
        forwardBtn.clicked[bool].connect(self.anyName('fowardBtn')) #point of connection (self.INSERT_FUNCTION_NAME_HERE)

        #backward
        backwardBtn = QPushButton('Backward', self)
        backwardBtn.setGeometry(QtCore.QRect(130, 427, 93, 51))
        backwardBtn.clicked[bool].connect(self.anyName('backwardBtn')) #point of connection (self.INSERT_FUNCTION_NAME_HERE)
        
        #right
        rightBtn = QPushButton('Right', self)
        rightBtn.setGeometry(QtCore.QRect(250, 377, 93, 51))
        rightBtn.clicked[bool].connect(self.anyName('rightBtn')) #point of connection (self.INSERT_FUNCTION_NAME_HERE)

        #left
        leftBtn = QPushButton('Left', self)
        leftBtn.setGeometry(QtCore.QRect(10, 377, 93, 51))
        leftBtn.clicked[bool].connect(self.anyName('leftBtn')) #point of connection (self.INSERT_FUNCTION_NAME_HERE)

        #up
        upBtn = QPushButton('Up', self)
        upBtn.setGeometry(QtCore.QRect(810, 327, 93, 61))
        upBtn.clicked[bool].connect(self.anyName('upBtn')) #point of connection (self.INSERT_FUNCTION_NAME_HERE)  

        #down
        downBtn = QPushButton('Down', self)
        downBtn.setGeometry(QtCore.QRect(810, 510, 93, 51))
        downBtn.clicked[bool].connect(self.anyName('downBtn')) #point of connection (self.INSERT_FUNCTION_NAME_HERE)

        #battery percentage
        batteryPercentage = QProgressBar(self)
        batteryPercentage.setGeometry(QtCore.QRect(30, 20, 201, 41))
        batteryPercentage.setProperty("value", 24) #SET VALUE OF BATTERY

        #ccW
        ccWBtn = QPushButton('CCW', self)
        ccWBtn.setGeometry(QtCore.QRect(630, 420, 181, 61))
        ccWBtn.clicked[bool].connect(self.anyName('ccWBtn')) #point of connection (self.INSERT_FUNCTION_NAME_HERE)

        #cW
        cWBtn = QPushButton('CW', self)
        cWBtn.setGeometry(QtCore.QRect(890, 420, 131, 61))
        cWBtn.clicked[bool].connect(self.anyName('cWBtn')) #point of connection (self.INSERT_FUNCTION_NAME_HERE)

        #set speed slider
        speedSlider = QSlider(self)
        speedSlider.setGeometry(QtCore.QRect(390, 250, 160, 22))
        speedSlider.setOrientation(QtCore.Qt.Horizontal)

        #speed value
        speedValue = QLCDNumber(self)
        speedValue.setGeometry(QtCore.QRect(350, 70, 281, 171))

        #takeoff
        takeoffBtn = QPushButton('Takeoff', self)
        takeoffBtn.setGeometry(QtCore.QRect(450, 320, 80, 61))
        takeoffBtn.clicked[bool].connect(self.anyName('takeoffdBtn')) #point of connection (self.INSERT_FUNCTION_NAME_HERE)

        #land
        landBtn = QPushButton('Land', self)
        landBtn.setGeometry(QtCore.QRect(450, 440, 80, 61))
        landBtn.clicked[bool].connect(self.anyName('landBtn')) #point of connection (self.INSERT_FUNCTION_NAME_HERE)

        self.setGeometry(300, 300, 300, 200)
        self.show()


def main():

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()