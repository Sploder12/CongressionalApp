# http://www.ryzerobotics.com/

import threading 
import socket
import sys
import time
import platform  

import constant

#class that contains all the data for the TelloSDK instance
class telloSDK:
    def __init__(self, port = 9001, host = ''):
        self.running = True

        self.port = port
        self.host = host
        self.locaddr = (host,port) 

        # Create a UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.tello_address = ('192.168.10.1', 8889)

        self.sock.bind(self.locaddr)

        #recvThread create
        self.recvThread = threading.Thread(target=self.recv)
        self.recvThread.start()

        self.sendMessage("command") #needed to be in command mode
  
    def recv(self):
        while self.recvThread.is_alive and self.running: 
            try:
                data, server = self.sock.recvfrom(1518)
                print(data.decode(encoding="utf-8"))
            except Exception as e:
                if(self.running):
                    print (str(e))
                    self.end(-2)
    
    #returns -1 if failed, 1 is sucessful
    def sendMessage(self, msg):
        try:
            if not msg:
                return -1  

            if 'end' in msg:
                self.end()
                return 1

            # Send data
            msg = msg.encode(encoding="utf-8") 
            sent = self.sock.sendto(msg, self.tello_address)
            return 1
        except KeyboardInterrupt:
            self.end(-1)
            return -1

    def end(self, errorNum = 0):
        self.sendMessage("land")
        self.running = False
        if(self.recvThread.is_alive):
            self.recvThread.join
        self.sock.close()
        #prints the exit code
        print("Ended Tello: " + constant.END_NUMS.get(errorNum, "ERROR NUM DOES NOT EXIST: "+str(errorNum)))