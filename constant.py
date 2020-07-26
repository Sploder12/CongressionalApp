import socket

#Messages when ending instances
END_NUMS = {
    -2 : "Bad Receive",
    -1 : "Interrupted",
     0 : "Normal End",
}

HOST_NAME = socket.gethostname()
LOCAL_IP = socket.gethostbyname(HOST_NAME)