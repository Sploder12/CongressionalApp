import sys
from tello import *
from Tello3 import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QWidget, QToolTip,
    QPushButton, QApplication, QProgressBar, QSlider, QLCDNumber)
from PyQt5.QtGui import QFont

instance = Tello3.telloSDK()
#where to end the instance???
class guiForDrone(QWidget):

    def forward(self):
        instance.sendMessage("forward 20")
    
    def backward(self):
        instance.sendMessage("backward 20")

    def right(self):
        instance.sendMessage("right 20")

    def left(self):
        instance.sendMessage("left 20")

    def up(self):
        instance.sendMessage("up 20")
    
    def down(self):
        instance.sendMessage("down 20")

    def ccW(self):
        instance.sendMessage("ccw 15")

    def cW(self):
        instance.sendMessage("cw 15")

    def speed(self, value):
        val = str(value)
        instance.sendMessage("speed " + val)

    def takeoff(self):
        instance.sendMessage("takeoff")

    def land(self):
        instance.sendMessage("land")

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tello Drone GUI")
        self.setFixedWidth(1280)
        self.setFixedHeight(720)

        self.initUI()


    def initUI(self):

        #forward
        forwardBtn = QPushButton('Forward', self)
        forwardBtn.setGeometry(QtCore.QRect(150, 430, 100, 50))
        forwardBtn.clicked[bool].connect(self.forward)

        #backward
        backwardBtn = QPushButton('Backward', self)
        backwardBtn.setGeometry(QtCore.QRect(150, 550, 100, 50))
        backwardBtn.clicked[bool].connect(self.backward)
        
        #right
        rightBtn = QPushButton('Right', self)
        rightBtn.setGeometry(QtCore.QRect(250, 490, 100, 50))
        rightBtn.clicked[bool].connect(self.right)

        #left
        leftBtn = QPushButton('Left', self)
        leftBtn.setGeometry(QtCore.QRect(50, 490, 100, 50))
        leftBtn.clicked[bool].connect(self.left)

        #up
        upBtn = QPushButton('Up', self)
        upBtn.setGeometry(QtCore.QRect(980, 430, 100, 50))
        upBtn.clicked[bool].connect(self.up)

        #down
        downBtn = QPushButton('Down', self)
        downBtn.setGeometry(QtCore.QRect(980, 550, 100, 50))
        downBtn.clicked[bool].connect(self.down)

        #battery percentage
        batteryPercentage = QProgressBar(self)
        batteryPercentage.setGeometry(QtCore.QRect(50, 50, 300, 75))
        batteryPercentage.setProperty("value", 24) #SET VALUE OF BATTERY

        #ccW
        ccWBtn = QPushButton('CCW', self)
        ccWBtn.setGeometry(QtCore.QRect(880, 490, 100, 50))
        ccWBtn.clicked[bool].connect(self.ccW) 

        #cW
        cWBtn = QPushButton('CW', self)
        cWBtn.setGeometry(QtCore.QRect(1080, 490, 100, 50))
        cWBtn.clicked[bool].connect(self.cW)

        #set speed slider
        speedSlider = QSlider(self)
        speedSlider.setMinimum(1)
        speedSlider.setMaximum(100)
        speedSlider.setValue(20)
        speedSlider.setTickPosition(QSlider.TicksBelow)
        speedSlider.setTickInterval(5)
        speedSlider.setGeometry(QtCore.QRect(390, 275, 500, 50))
        speedSlider.setOrientation(QtCore.Qt.Horizontal)
        speedSlider.valueChanged.connect(self.speed)

        #speed value
        speedValue = QLCDNumber(self)
        speedValue.setGeometry(QtCore.QRect(490, 100, 300, 150))

        #takeoff
        takeoffBtn = QPushButton('Takeoff', self)
        takeoffBtn.setGeometry(QtCore.QRect(590, 465, 100, 50))
        takeoffBtn.clicked[bool].connect(self.takeoff)

        #land
        landBtn = QPushButton('Land', self)
        landBtn.setGeometry(QtCore.QRect(590, 525, 100, 50))
        landBtn.clicked[bool].connect(self.land)

        self.setGeometry(300, 300, 300, 200)
        self.show()


def main():

    app = QApplication(sys.argv)
    ex = guiForDrone()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()