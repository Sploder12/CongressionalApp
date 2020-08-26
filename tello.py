import Tello3
import cv2

#instance of Tello3 
instance = Tello3.telloSDK() #will end if it can't connect to Tello (see ln 42/43 of Tello3.py)
#if program hangs expect ln 42/43 of Tello3.py

while(instance.running):
    img = instance.getImage() #example: set frame to img
    cv2.imshow('image',img)
    cv2.waitKey(100)

instance.sendMessage("forward 20") #example: moves Tello forward 20cm

instance.end() #Make sure you end it when done!
cv2.destroyAllWindows()
