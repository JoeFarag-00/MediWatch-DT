from Eat import *
from Sleep import *
import socket

class Soft_Behavior_Detector:
    def __init__(self, Connect = False):
        if(Connect == True):
            self.Socket = True
            self.Host, self.Port = "127.0.0.1", 8500
            self.Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.Sock.connect((self.Host, self.Port))
        else:
            self.Socket = False
        
        self.Eat = Eating_Detector()
        self.Sleep = Sleeping_Detector()

    def Classify(self, Frame):
        self.Sleep.Process_Frames(Frame)
        self.Flag_Sleeping = self.Sleep.Flag_Sleep

        if self.Flag_Sleeping == self.Sleep.Status_Awake:
            self.Eat.Process_Frames(Frame)
            self.Flag_Eating = self.Eat.Flag_Eating
        else:
            self.Flag_Eating = "None"

        if(self.Socket == True):
            Status = f"{self.Flag_Sleeping}, {self.Flag_Eating}"
            self.Sock.sendall(Status.encode("UTF-8"))