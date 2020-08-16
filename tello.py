import Tello3
import cv2
import math

#gets the frame in a safe way.
#Program will temporarily hang if reciever is writing the image
def getImage(instance):
    instance.mutexLock.acquire()
    frame = instance.Bframe
    instance.mutexLock.release()
    return frame

# Flys in a polygon shape starting on the bottom leftmost pont
#_in_ size : number 20 - 500 (centimeters)
#_in_ sides : integer 3 - 360
#_in_ instance : telloSDK instance
#
#_out_ status : bool -1?1
def flyPolygon(size, sides, instance):
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
#_in_ size : number 50 - 500
#_in_ instance : telloSDK instance
#
#_out_ status : bool -1?1
def figure8(size, instance):
    if(size < 50 or size > 500):
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
        instance.sendMessage("curve " + str(pnt1[0]) + " 0 " + str(pnt1[1]) + " " + str(pnt2[0]) + " 0 " + str(pnt2[1]))
    
    pnt1 = (x(0.25*math.pi), y(0.25*math.pi) - size) 
    pnt2 = (x(0.5*math.pi), y(0.5*math.pi) - size)
    for i in range(4): #second circle
        instance.sendMessage("curve " + str(pnt1[0]) + " 0 " + str(pnt1[1]) + " " + str(pnt2[0]) + " 0 " + str(pnt2[1]))

    return 1