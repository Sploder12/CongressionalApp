import Tello3
import cv2

#gets the frame in a safe way.
#Program will temporarily hang if reciever is writing the image
def getImage(instance):
    instance.mutexLock.acquire()
    frame = instance.Bframe
    instance.mutexLock.release()
    return frame

#instance of Tello3
#instance = Tello3.telloSDK()

#img = getImage(instance)

#Make sure you end it when done!
#instance.end()

