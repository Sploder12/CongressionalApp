import Tello3
import cv2

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
