import sys
import Tello3
import tello
import math
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QWidget, QToolTip,
    QPushButton, QApplication, QProgressBar, QSlider, QLCDNumber, QLabel)
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

    # def getspeed(self):
    #     speed = instance.sendMessage("speed?")
    #     return speed

    # def getbattery(self):
    #     battery = instance.sendMessage("battery?")
    #     return battery

    # def gettime(self):
    #     time = instance.sendMessage("time?")
    #     return time

    # def getheight(self):
    #     height = instance.sendMessage("height?")
    #     return height

    # def gettemp(self):
    #     temp = instance.sendMessage("temp?")
    #     return temp

    # def getattitude(self):
    #     attitude = instance.sendMessage("attitude?")
    #     return attitude

    # def getbarometer(self):
    #     barometer = instance.sendMessage("baro?")
    #     return barometer

    # def getacceleration(self):
    #     acceleration = instance.sendMessage("acceleration?")
    #     return acceleration

    # def gettof(self):
    #     tof = instance.sendMessage("tof?") # idk what tof is
    #     return tof
        
    # def getwifi(self):
    #     wifi = instance.sendMessage("wifi?")
    #     return wifi

    # def flyPolygon(self):
    #     sides = 5
    #     size = 150
    #     if(sides > 360 or sides < 3):
    #         return -1
    #     if(size > 500 or size < 20):
    #         return -1

    #     rotation = 360/sides
    #     if(sides != 4):
    #         if(sides == 3): 
    #             instance.sendMessage("cw 30")
    #         else:
    #             instance.sendMessage("ccw " + str(90-rotation))

    #     for i in range(sides):
    #         instance.sendMessage("forward " + str(size))
    #         if i == sides:
    #             instance.sendMessage("cw 90") #drone ends the same way it starts
    #         else:
    #             instance.sendMessage("cw " + str(rotation))
    #     return 1

    # #Flys in a figure 8 starting the the middle
    # #_in_ instance : telloSDK instance
    # #_in_ size : number 50 - 500
    # #_in_ speed : number 10-60 cm/s
    # #
    # #_out_ status : bool -1?1
    # def figure8(self):
    #     size = 150
    #     speed = 50
    #     if(size < 50 or size > 500):
    #         return -1
    #     if(speed < 10 or speed > 60):
    #         return -1

    #     #we're heavily assuming that curve uses relative postion instead of some magical absolute position that makes life suck (documentation is unclear)
    #     #also assuming that the drone's x/y/z axis are also relative to rotation
    #     #5% chance this works as is
    #     instance.sendMessage("cw 90")
    #     x = lambda rad: math.sin(rad)*size
    #     y = lambda rad: math.cos(rad)*size
    #     pnt1 = (x(0.25*math.pi), y(1.25*math.pi) + size) 
    #     pnt2 = (x(0.5*math.pi), y(0.5*math.pi) + size)
    #     for i in range(4): #first circle
    #         instance.sendMessage("curve " + str(pnt1[0]) + " 0 " + str(pnt1[1]) + " " + str(pnt2[0]) + " 0 " + str(pnt2[1]) + " " + str(speed))

    #     pnt1 = (x(0.25*math.pi), y(0.25*math.pi) - size) 
    #     pnt2 = (x(0.5*math.pi), y(0.5*math.pi) - size)
    #     for i in range(4): #second circle
    #         instance.sendMessage("curve " + str(pnt1[0]) + " 0 " + str(pnt1[1]) + " " + str(pnt2[0]) + " 0 " + str(pnt2[1]) + " " + str(speed))

    #     return 1
        
    def __init__(self):
        super().__init__()
        global instance

        self.setWindowTitle("Tello Drone GUI")
        self.setFixedWidth(1280)
        self.setFixedHeight(720)

        # self.speedLabel = QtWidgets.QLabel('Speed: ', self)
        # self.batteryLabel = QtWidgets.QLabel('Battery: ', self)
        # self.timeLabel = QtWidgets.QLabel('Time: ', self)
        # self.heightLabel = QtWidgets.QLabel('Height: ', self)
        # self.tempLabel = QtWidgets.QLabel('Temp: ', self)
        # self.attitudeLabel = QtWidgets.QLabel('Attitude: ', self)
        # self.barometerLabel = QtWidgets.QLabel('Barometer: ', self)
        # self.accelerationLabel = QtWidgets.QLabel('Acceleration: ', self)
        # self.tofLabel = QtWidgets.QLabel('TOF: ', self)
        # self.wifiLabel = QtWidgets.QLabel('Wifi: ', self)

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

        # self.speedLabel = QtWidgets.QLabel('Speed: ', self)
        # self.speedLabel.setGeometry(QtCore.QRect(900, 10, 75, 20))

        # self.batteryLabel = QtWidgets.QLabel('Battery: ', self)
        # self.batteryLabel.setGeometry(QtCore.QRect(900, 35, 75, 20))

        # self.timeLabel = QtWidgets.QLabel('Time: ', self)
        # self.timeLabel.setGeometry(QtCore.QRect(900, 60, 75, 20))

        # self.heightLabel = QtWidgets.QLabel('Height: ', self)
        # self.heightLabel.setGeometry(QtCore.QRect(900, 85, 75, 20))

        # self.tempLabel = QtWidgets.QLabel('Temp: ', self)
        # self.tempLabel.setGeometry(QtCore.QRect(900, 110, 75, 20))

        # self.attitudeLabel = QtWidgets.QLabel('Attitude: ', self)
        # self.attitudeLabel.setGeometry(QtCore.QRect(900, 135, 75, 20))

        # self.barometerLabel = QtWidgets.QLabel('Barometer: ', self)
        # self.barometerLabel.setGeometry(QtCore.QRect(900, 160, 75, 20))

        # self.accelerationLabel = QtWidgets.QLabel('Acceleration: ', self)
        # self.accelerationLabel.setGeometry(QtCore.QRect(900, 185, 81, 20))

        # self.tofLabel = QtWidgets.QLabel('TOF: ', self)
        # self.tofLabel.setGeometry(QtCore.QRect(900, 210, 75, 20))

        # self.wifiLabel = QtWidgets.QLabel('Wifi: ', self)
        # self.wifiLabel.setGeometry(QtCore.QRect(900, 235, 75, 20))

        # flyPolygonBtn = QtWidgets.QPushButton('Fly Polygon', self)
        # flyPolygonBtn.setGeometry(QtCore.QRect(490, 660, 100, 30))
        # flyPolygonBtn.clicked[bool].connect(self.flyPolygon)

        # sidesPolygon = QtWidgets.QSpinBox(self)
        # sidesPolygon.setGeometry(QtCore.QRect(490, 630, 42, 22))

        # label = QtWidgets.QLabel('Size', self)
        # label.setGeometry(QtCore.QRect(490, 610, 55, 16))

        # sizePolygon = QtWidgets.QSpinBox(self)
        # sizePolygon.setGeometry(QtCore.QRect(560, 630, 42, 22))

        # label_2 = QtWidgets.QLabel('Sides', self)
        # label_2.setGeometry(QtCore.QRect(560, 610, 55, 16))
        
        # figure8Btn = QtWidgets.QPushButton('Figure 8', self)
        # figure8Btn.setGeometry(QtCore.QRect(680, 660, 100, 30))
        # figure8Btn.clicked[bool].connect(self.figure8)

        # label_3 = QtWidgets.QLabel('Size', self)
        # label_3.setGeometry(QtCore.QRect(670, 610, 55, 16))

        # size8 = QtWidgets.QSpinBox(self)
        # size8.setGeometry(QtCore.QRect(740, 630, 42, 22))

        # label_4 = QtWidgets.QLabel('Sides', self)
        # label_4.setGeometry(QtCore.QRect(740, 610, 55, 16))

        # sides8 = QtWidgets.QSpinBox(self)
        # sides8.setGeometry(QtCore.QRect(670, 630, 42, 22))

        # self.updateLabels()
        # self.my_timer = QtCore.QTimer()
        # self.my_timer.timeout.connect(self.updateLabels)
        # self.my_timer.start(5000) #5sec interval 

        self.setGeometry(300, 300, 300, 200)
        self.show()

    # def updateLabels(self):
    #     speed = "Speed: " + str(self.getspeed())
    #     battery = "Battery: " + str(self.getbattery())
    #     time = str(self.gettime())
    #     height = str(self.getheight())
    #     temp = str(self.gettemp())
    #     attitude = str(self.getattitude())
    #     barometer = str(self.getbarometer())
    #     acceleration = str(self.getacceleration())
    #     tof = str(self.gettof())
    #     wifi = str(self.getwifi())
    #     self.speedLabel.setText(speed)
    #     self.batteryLabel.setText(battery)
    #     self.timeLabel.setText(time)
    #     self.heightLabel.setText(height)
    #     self.tempLabel.setText(temp)
    #     self.attitudeLabel.setText(attitude)
    #     self.barometerLabel.setText(barometer)
    #     self.accelerationLabel.setText(acceleration)
    #     self.tofLabel.setText(tof)
    #     self.wifiLabel.setText(wifi)
    #     self.update()

def main():

    app = QApplication(sys.argv)
    ex = guiForDrone()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

instance.end()