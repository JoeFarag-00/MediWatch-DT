from Eat import *
from Sleep import *
from Facial_Expression import *
from Gaze_Track import *
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
        self.Facial_Expression = Facial_Expression_Classifier()
        self.Gaze_Tracking = Gaze_Tracking()

    def Classify(self, Frame):
        self.Sleep.Process_Frames(Frame)
        self.Flag_Sleeping = self.Sleep.Flag_Sleep

        if self.Flag_Sleeping == self.Sleep.Status_Awake:
            self.Eat.Process_Frames(Frame)
            self.Facial_Expression.Process_Frames(Frame)
            self.Gaze_Tracking.Process_Frames(Frame)
            self.Flag_Eating = self.Eat.Flag_Eating
            self.Expression_Status = self.Facial_Expression.Expression_Status
            self.Eye_X = self.Gaze_Tracking.Average_Eye_X
            self.Eye_Y = self.Gaze_Tracking.Average_Eye_Y
            self.Eye_X_Frame_Coordinate = self.Gaze_Tracking.Left_Center
            self.Eye_Y_Frame_Coordinate = self.Gaze_Tracking.Right_Center

        else:
            self.Flag_Eating = "None"
            self.Expression_Status = "None"
            self.Eye_X = "None"
            self.Eye_Y = "None"
            self.Eye_X_Frame_Coordinate = "None"
            self.Eye_Y_Frame_Coordinate = "None"