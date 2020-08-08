import Tello3

#instance of Tello3 
instance = Tello3.telloSDK() #will end if it can't connect to Tello (see ln 42/43 of Tello3.py)
#if program hangs expect ln 42/43 of Tello3.py

img = instance.getImage() #example: set frame to img

print(img)

instance.sendMessage("forward 20") #example: moves Tello forward 20cm

instance.end() #Make sure you end it when done!

