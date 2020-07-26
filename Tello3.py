# http://www.ryzerobotics.com/

import threading 
import socket
import numpy as np
import libh264decoder

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
        self.sock_video = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.tello_address = (constant.LOCAL_IP, 8889)

        self.sock.bind(self.locaddr)

        self.local_video_port = 11111

        self.mutexLock = threading.Lock() #yay mutual exclusion
        self.decoder = libh264decoder.H264Decoder()
        self.Bframe = None

        #recvThread create
        self.recvThread = threading.Thread(target=self.recv)
        self.recvThread.start()

        self.sendMessage("command") #needed to be in command mode

        self.sendMessage("streamon")

        self.sock_video.bind((constant.LOCAL_IP, self.local_video_port))

        # thread for receiving video
        self.recvVidThread = threading.Thread(target=self.recvVid)

        self.recvVidThread.start()
  
    def recv(self):
        while self.recvThread.is_alive and self.running: 
            try:
                data, server = self.sock.recvfrom(1518)
                print(data.decode(encoding="utf-8"))

            except Exception as e:
                if(self.running):
                    print (str(e))
                    self.end(-2)
    
    def recvVid(self):
        """
        Listens for video streaming (raw h264) from the Tello.
        Runs as a thread, sets self.Bframe to the most recent frame Tello captured.
        """
        packet_data = ""
        while self.recvVidThread.is_alive and self.running:
            try:
                res_string, ip = self.sock_video.recvfrom(2048)
                packet_data += res_string

                #Prevents writing an image while reading
                if(self.mutexLock.acquire(False)): #blocking is disabled so it will write the latest frames instead of waiting with an old frames
                    if len(res_string) != 1460:
                        for frame in self._h264_decode(packet_data):
                            self.Bframe = frame
                        packet_data = ""
                    self.mutexLock.release()

            except Exception as e:
                if(self.running):
                    print(str(e))
                    self.end(-2)
    
    def _h264_decode(self, packet_data):
        """
        :param packet_data: raw h264 data array
       
        :return: a list of decoded frame
        """
        res_frame_list = []
        frames = self.decoder.decode(packet_data)
        for framedata in frames:
            (frame, w, h, ls) = framedata
            if frame is not None:
                # print 'frame size %i bytes, w %i, h %i, linesize %i' % (len(frame), w, h, ls)

                frame = np.fromstring(frame, dtype=np.ubyte, count=len(frame), sep='')
                frame = (frame.reshape((h, ls / 3, 3)))
                frame = frame[:, :w, :]
                res_frame_list.append(frame)

        return res_frame_list

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
            return self.sock.sendto(msg, self.tello_address) #returns number of bytes sent
        except KeyboardInterrupt:
            self.end(-1)
            return -1

    def end(self, errorNum = 0):
        self.sendMessage("land")
        self.running = False
        if(self.recvThread.is_alive):
            self.recvThread.join
        if(self.recvVidThread.is_alive):
            self.recvThread.join
        self.sock.close()
        #prints the exit code
        print("Ended Tello: " + constant.END_NUMS.get(errorNum, "ERROR NUM DOES NOT EXIST: "+str(errorNum)))