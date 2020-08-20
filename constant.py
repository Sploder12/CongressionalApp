import socket

#Messages when ending instances
END_NUMS = {
    -3 : "Failed To Open Camera",
    -2 : "Bad Receive",
    -1 : "Interrupted",
     0 : "Normal End",
}

HOST_NAME = socket.gethostname()
LOCAL_IP = socket.gethostbyname(HOST_NAME)
TELLO_IP = "192.168.10.1" 

TELLO_CAMERA_THETA = 0 #angle of depression for camera