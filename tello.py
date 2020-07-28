import Tello3

#gets the frame in a safe way.
#Program will temporarily hang if reciever is writing the image
frame = None
def updateImage(instance):
    global frame
    instance.mutexLock.aquire()
    if(instance.BFrame == None):
        instance.mutexLock.release()
        return -1
    else:    
        frame = instance.BFrame
        instance.mutexLock.release()
        return 1

#instance of Tello3
instance = Tello3.telloSDK()

#Make sure you end it when done!
instance.end()