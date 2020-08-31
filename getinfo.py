import Tello3
instance = Tello3.telloSDK()
class getinfo:
    def getspeed(self):
        speed = instance.sendMessage("speed?")
        return speed
    def getbattery(self):
        battery = instance.sendMessage("battery?")
        return battery
    def gettime(self):
        time = instance.sendMessage("time?")
        return time
    def getheight(self):
        height = instance.sendMessage("height?")
        return height
    def gettemp(self):
        temp = instance.sendMessage("temp?")
        return temp
    def getattitude(self):
        attitude = instance.sendMessage("attitude?")
        return attitude
    def getbarometer(self):
        barometer = instance.sendMessage("baro?")
        return barometer
    def getacceleration(self):
        acceleration = instance.sendMessage("acceleration?")
        return acceleration
    def gettof(self):
        tof = instance.sendMessage("tof?") # idk what tof is
        return tof
    def getwifi(self):
        wifi = instance.sendMessage("wifi?")
        return wifi