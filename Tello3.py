# http://www.ryzerobotics.com/
import threading 
import socket
import cv2
import constant

#class that contains all the data for the TelloSDK instance
class telloSDK:
    def __init__(self, port = 8889, host = ''):
        self.running = True

        self.port = port
        self.host = host

        # Create a UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.tello_address = (constant.TELLO_IP, port) #change TELLO_IP to LOCAL_IP if testing without drone

        self.sock.bind((constant.LOCAL_IP, port))

        self.local_video_port = 11111

        self.mutexLock = threading.Lock() #yay mutual exclusion
        self.endLock = threading.Lock()

        self.startWait = threading.Condition()
        self.msgWait = threading.Condition() #cool anti-busy waiting technique

        self.response = None
        self.Bframe = None

        self.command_timeout = 0.3

        #create recieve thread
        self.recvThread = threading.Thread(target=self.recv)
        self.recvThread.start()

        self.sendMessage("command") #needed to be in command mode
        self.sendMessage("streamon") #starts video stream

        self.ret = False
        #self.telloVideo = cv2.VideoCapture("udp://@" + constant.TELLO_IP + ":" + str(self.local_video_port))
        self.telloVideo = cv2.VideoCapture("test.mp4") #used for testing when Tello not present
        self.scale = 3

        #create video thread
        self.recvVidThread = threading.Thread(target=self.recvVid)
        if not self.telloVideo.isOpened():
            self.end(-3)
        else:
            self.recvVidThread.start()
            self.startWait.acquire()
            self.startWait.wait(5)
            self.startWait.release()
            
  
    def __del__(self):
        self.sock.close()
        self.telloVideo.release()
        self.running = False
        
    def recv(self):
        while self.recvThread.is_alive and self.running: 
            try:
                self.response, server = self.sock.recvfrom(3000)
                print(self.response.decode(encoding="utf-8"))
                
                self.msgWait.acquire()
                self.msgWait.notify() #tell the main thread it can wake up
                self.msgWait.release()
            except Exception as e:
                if(type(e) == ConnectionResetError):
                    print("Reseting Receive Data Connection")
                    self.sock.close()
                    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    self.sock.bind((constant.LOCAL_IP, self.port))

                elif(self.running):
                    print(e)
                    self.end(-2)
    
    def recvVid(self):
        """
        Runs as a thread, sets self.Bframe to the most recent frame Tello captured.
        """
        while self.recvVidThread.is_alive and self.running:
            try:
                self.ret, frame = self.telloVideo.read()

                if(self.ret):
                    #Prevents writing an image while reading
                    if(self.mutexLock.acquire(False)): #blocking is disabled so it will write the latest frames instead of waiting with an old frames
                        height , width , layers =  frame.shape
                        new_h=int(height/self.scale)
                        new_w=int(width/self.scale)
                        self.Bframe = cv2.resize(frame, (new_w, new_h)) #resizes image
                        #cv2.imwrite("opt.png", self.Bframe)
                        self.mutexLock.release()

                        self.startWait.acquire()
                        self.startWait.notify()
                        self.startWait.release()

            except Exception as e:
                print(str(e))
                self.end(-2)
        self.telloVideo.release()
    
    def getImage(self):
        self.mutexLock.acquire()
        frame = self.Bframe
        self.mutexLock.release()
        return frame


    #returns -1 if failed, 1 is sucessful
    def sendMessage(self, msg):
        if self.running:
            try:
                if not msg:
                    return -1  

                if 'end' in msg:
                    self.end()
                    return 1

                # Send data
                msg = msg.encode(encoding="utf-8") 
                data = self.sock.sendto(msg, self.tello_address) #returns number of bytes sent

                #A non busy wait for response
                if(self.response is None):
                    self.msgWait.acquire()
                    self.msgWait.wait(self.command_timeout)
                    self.msgWait.release()                

                #using the same if condition may seem redundant but response changes inbetween them thanks to multithreading
                if self.response is None:
                    response = 'none_response'
                else:
                    try:
                        response = self.response.decode('utf-8')
                    except Exception as e:
                        print("Response couldn't be decoded")

                self.response = None

                return response
            except KeyboardInterrupt:
                self.end(-1)
                return -1

    def end(self, errorNum = 0):
        self.endLock.acquire() #prevents several threads using end() at the same time
        if self.running:
            self.sendMessage("land")
            self.running = False
            if(self.recvThread.is_alive):
                self.recvThread.join
            self.sock.close()
            if(self.recvVidThread.is_alive):
                self.recvThread.join
            #prints the exit code
            print("Ended Tello: " + constant.END_NUMS.get(errorNum, "ERROR NUM DOES NOT EXIST: "+str(errorNum)))
        else:
            print("Attempted To End Already Ended Tello Instance With Code " + str(errorNum))
        self.endLock.release()