import sys
import Tello3
import tello
import math
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QWidget, QToolTip,
    QPushButton, QApplication, QProgressBar, QSlider, QLCDNumber, QLabel)
from PyQt5.QtGui import QFont

instance = Tello3.telloSDK()
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

    def flyPolygon(self):
        sides = 5
        size = 150
        if(sides > 360 or sides < 3):
            return -1
        if(size > 500 or size < 20):
            return -1

        rotation = 360/sides
        if(sides != 4):
            if(sides == 3): 
                instance.sendMessage("cw 30")
            else:
                instance.sendMessage("ccw " + str(90-rotation))

        for i in range(sides):
            instance.sendMessage("forward " + str(size))
            if i == sides:
                instance.sendMessage("cw 90") #drone ends the same way it starts
            else:
                instance.sendMessage("cw " + str(rotation))
        return 1

    #Flys in a figure 8 starting the the middle
    #_in_ instance : telloSDK instance
    #_in_ size : number 50 - 500
    #_in_ speed : number 10-60 cm/s
    #
    #_out_ status : bool -1?1
    def figure8(self):
        size = 150
        speed = 50
        if(size < 50 or size > 500):
            return -1
        if(speed < 10 or speed > 60):
            return -1

        #we're heavily assuming that curve uses relative postion instead of some magical absolute position that makes life suck (documentation is unclear)
        #also assuming that the drone's x/y/z axis are also relative to rotation
        #5% chance this works as is
        instance.sendMessage("cw 90")
        x = lambda rad: math.sin(rad)*size
        y = lambda rad: math.cos(rad)*size
        pnt1 = (x(0.25*math.pi), y(1.25*math.pi) + size) 
        pnt2 = (x(0.5*math.pi), y(0.5*math.pi) + size)
        for i in range(4): #first circle
            instance.sendMessage("curve " + str(pnt1[0]) + " 0 " + str(pnt1[1]) + " " + str(pnt2[0]) + " 0 " + str(pnt2[1]) + " " + str(speed))

        pnt1 = (x(0.25*math.pi), y(0.25*math.pi) - size) 
        pnt2 = (x(0.5*math.pi), y(0.5*math.pi) - size)
        for i in range(4): #second circle
            instance.sendMessage("curve " + str(pnt1[0]) + " 0 " + str(pnt1[1]) + " " + str(pnt2[0]) + " 0 " + str(pnt2[1]) + " " + str(speed))

        return 1
        
    def __init__(self):
        super().__init__()
        global instance

        self.setWindowTitle("Tello Drone GUI")
        self.setFixedWidth(1280)
        self.setFixedHeight(720)

        self.pitchLabel = QtWidgets.QLabel("pitch: ", self)
        self.rollLabel = QtWidgets.QLabel("roll: ", self)
        self.yawLabel = QtWidgets.QLabel("yaw: ", self)
        self.pitchLabel = QtWidgets.QLabel("pitch: ", self)
        self.xSpeedLabel = QtWidgets.QLabel("xSpeed: ", self)
        self.ySpeedLabel = QtWidgets.QLabel("ySpeed: ", self)
        self.zSpeedLabel = QtWidgets.QLabel("zSpeed: ", self)
        self.lowestTempLabel = QtWidgets.QLabel("lowestTemp: ", self)
        self.highestTempLabel = QtWidgets.QLabel("highestTemp: ", self)
        self.barometerLabel = QtWidgets.QLabel("barometer: ", self)
        self.TOFLabel = QtWidgets.QLabel("TOF: ", self)
        self.batteryLabel = QtWidgets.QLabel("battery: ", self)
        self.motorTimeLabel = QtWidgets.QLabel("motorTime: ", self)
        self.heightLabel = QtWidgets.QLabel("height: ", self)
        self.xAccelLabel = QtWidgets.QLabel("xAccel: ", self)
        self.yAccelLabel = QtWidgets.QLabel("yAccel: ", self)
        self.zAccelLabel = QtWidgets.QLabel("zAccel: ", self)

        self.speedValue = QLCDNumber(self)
        self.batteryPercentage = QProgressBar(self)


        self.initUI()


    def initUI(self):
        global instance

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
        self.batteryPercentage = QProgressBar(self)
        self.batteryPercentage.setGeometry(QtCore.QRect(50, 50, 300, 75))
        self.batteryPercentage.setProperty("value", 24) #SET VALUE OF BATTERY

        #ccW
        ccWBtn = QPushButton('CCW', self)
        ccWBtn.setGeometry(QtCore.QRect(880, 490, 100, 50))
        ccWBtn.clicked[bool].connect(self.ccW) 

        #cW
        cWBtn = QPushButton('CW', self)
        cWBtn.setGeometry(QtCore.QRect(1080, 490, 100, 50))
        cWBtn.clicked[bool].connect(self.cW)

        # #set speed slider
        # speedSlider = QSlider(self)
        # speedSlider.setMinimum(1)
        # speedSlider.setMaximum(100)
        # speedSlider.setValue(20)
        # speedSlider.setTickPosition(QSlider.TicksBelow)
        # speedSlider.setTickInterval(5)
        # speedSlider.setGeometry(QtCore.QRect(390, 275, 500, 50))
        # speedSlider.setOrientation(QtCore.Qt.Horizontal)
        # speedSlider.valueChanged.connect(self.speed)

        #speed value
        self.speedValue = QLCDNumber(self)
        self.speedValue.setGeometry(QtCore.QRect(490, 100, 300, 150))

        #takeoff
        takeoffBtn = QPushButton('Takeoff', self)
        takeoffBtn.setGeometry(QtCore.QRect(590, 465, 100, 50))
        takeoffBtn.clicked[bool].connect(self.takeoff)

        #land
        landBtn = QPushButton('Land', self)
        landBtn.setGeometry(QtCore.QRect(590, 525, 100, 50))
        landBtn.clicked[bool].connect(self.land)

        # self.speedLabel = QtWidgets.QLabel('Speed: ', self)
        self.pitchLabel = QtWidgets.QLabel("pitch", self)
        self.pitchLabel.setGeometry(QtCore.QRect(900, 10, 350, 20))

        self.rollLabel = QtWidgets.QLabel("roll", self)
        self.rollLabel.setGeometry(QtCore.QRect(900, 35, 350, 20))

        self.yawLabel = QtWidgets.QLabel("yaw", self)
        self.yawLabel.setGeometry(QtCore.QRect(900, 60, 350, 20))

        self.xSpeedLabel = QtWidgets.QLabel("xSpeed", self)
        self.xSpeedLabel.setGeometry(QtCore.QRect(900, 85, 3505, 20))

        self.ySpeedLabel = QtWidgets.QLabel("ySpeed", self)
        self.ySpeedLabel.setGeometry(QtCore.QRect(900, 110, 350, 20))

        self.zSpeedLabel = QtWidgets.QLabel("zSpeed", self)
        self.zSpeedLabel.setGeometry(QtCore.QRect(900, 135, 350, 20))

        self.lowestTempLabel = QtWidgets.QLabel("lowestTemp", self)
        self.lowestTempLabel.setGeometry(QtCore.QRect(900, 160, 350, 20))

        self.highestTempLabel = QtWidgets.QLabel("highestTemp", self)
        self.highestTempLabel.setGeometry(QtCore.QRect(900, 185, 350, 20))

        self.barometerLabel = QtWidgets.QLabel("barometer", self)
        self.barometerLabel.setGeometry(QtCore.QRect(900, 210, 75, 20))

        self.TOFLabel = QtWidgets.QLabel("TOF", self)
        self.TOFLabel.setGeometry(QtCore.QRect(900, 235, 350, 20))

        self.batteryLabel = QtWidgets.QLabel("batter", self)
        self.batteryLabel.setGeometry(QtCore.QRect(900, 260, 350, 20))

        self.motorTimeLabel = QtWidgets.QLabel("motorTime", self)
        self.motorTimeLabel.setGeometry(QtCore.QRect(900, 285, 350, 20))

        self.heightLabel = QtWidgets.QLabel("height", self)
        self.heightLabel.setGeometry(QtCore.QRect(900, 310, 350, 20))

        self.xAccelLabel = QtWidgets.QLabel("xAccel", self)
        self.xAccelLabel.setGeometry(QtCore.QRect(900, 335, 350, 20))

        self.yAccelLabel = QtWidgets.QLabel("yAccel", self)
        self.yAccelLabel.setGeometry(QtCore.QRect(900, 360, 350, 20))

        self.zAccelLabel = QtWidgets.QLabel("zAccel", self)
        self.zAccelLabel.setGeometry(QtCore.QRect(900, 385, 350, 20))

        flyPolygonBtn = QtWidgets.QPushButton('Fly Polygon', self)
        flyPolygonBtn.setGeometry(QtCore.QRect(490, 660, 100, 30))
        flyPolygonBtn.clicked[bool].connect(self.flyPolygon)

        sidesPolygon = QtWidgets.QSpinBox(self)
        sidesPolygon.setGeometry(QtCore.QRect(490, 630, 42, 22))

        label = QtWidgets.QLabel('Size', self)
        label.setGeometry(QtCore.QRect(490, 610, 55, 16))

        sizePolygon = QtWidgets.QSpinBox(self)
        sizePolygon.setGeometry(QtCore.QRect(560, 630, 42, 22))

        label_2 = QtWidgets.QLabel('Sides', self)
        label_2.setGeometry(QtCore.QRect(560, 610, 55, 16))
        
        figure8Btn = QtWidgets.QPushButton('Figure 8', self)
        figure8Btn.setGeometry(QtCore.QRect(680, 660, 100, 30))
        figure8Btn.clicked[bool].connect(self.figure8)

        label_3 = QtWidgets.QLabel('Size', self)
        label_3.setGeometry(QtCore.QRect(670, 610, 55, 16))

        size8 = QtWidgets.QSpinBox(self)
        size8.setGeometry(QtCore.QRect(740, 630, 42, 22))

        label_4 = QtWidgets.QLabel('Sides', self)
        label_4.setGeometry(QtCore.QRect(740, 610, 55, 16))

        sides8 = QtWidgets.QSpinBox(self)
        sides8.setGeometry(QtCore.QRect(670, 630, 42, 22))

        self.updateLabels()
        self.my_timer = QtCore.QTimer()
        self.my_timer.timeout.connect(self.updateLabels)
        self.my_timer.start(5000) #5sec interval 

        self.setGeometry(300, 300, 300, 200)
        self.show()

    def proper_round(num, dec=0):
        num = str(num)[:str(num).index('.')+dec+2]
        if num[-1]>='5':
            return float(num[:-2-(not dec)]+str(int(num[-2-(not dec)])+1))
        return float(num[:-1])    

    def updateLabels(self):
        info = instance.getDat()
        pitch = "pitch" + str(info['pitch'])
        roll = "roll" + str(info['roll'])
        yaw = "yaw" + str(info['yaw'])
        xSpeed = "xSpeed" + str(info['xSpeed'])
        ySpeed = "ySpeed" + str(info['ySpeed'])
        zSpeed = "zSpeed" + str(info["zSpeed"])
        lowestTemp = "lowestTemp" + str(info['lowestTemp'])
        highestTemp = "highestTemp" + str(info['highestTemp'])
        barometer = "barometer" + str(info['barometer'])
        TOF = "TOF" + str(info['TOF'])
        battery = "battery" + str(info['battery%'])
        motorTime = "motorTime" + str(info['motorTime'])
        height = "height" + str(info['height'])
        xAccel = "xAccel" + str(info['xAccel'])
        yAccel = "yAccel" + str(info['yAccel'])
        zAccel = "zAccel" + str(info['zAccel'])
        self.pitchLabel.setText(pitch)
        self.rollLabel.setText(roll)
        self.yawLabel.setText(yaw)
        self.xSpeedLabel.setText(xSpeed)
        self.ySpeedLabel.setText(ySpeed)
        self.zSpeedLabel.setText(zSpeed)
        self.lowestTempLabel.setText(lowestTemp)
        self.highestTempLabel.setText(highestTemp)
        self.barometerLabel.setText(barometer)
        self.TOFLabel.setText(TOF)
        self.batteryLabel.setText(battery)
        self.motorTimeLabel.setText(motorTime)
        self.heightLabel.setText(height)
        self.xAccelLabel.setText(xAccel)
        self.yAccelLabel.setText(yAccel)
        self.zAccelLabel.setText(zAccel)

        self.batteryPercentage.setProperty("value", info['battery%']) #SET VALUE OF BATTERY
        self.speedValue.intValue(math.floor((info['xSpeed'])))
        
        self.update()

def main():

    app = QApplication(sys.argv)
    ex = guiForDrone()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

instance.end()