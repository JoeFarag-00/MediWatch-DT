import cv2
from deepface import DeepFace 
import time

class Facial_Expression_Classifier:
    def __init__(self, Path = "", Connect = False):
        self.Path = Path
        if len(Path) > 0:
            self.Capture = cv2.VideoCapture(Path)
        else:
            self.Capture = cv2.VideoCapture(0)
        
        self.Start_Time = 0
        self.Check_Expression_Timer = 1
        self.Expression_Status = "neutral"

    def Classify(self):
        self.Result = DeepFace.analyze(self.Frame, actions=['emotion'], enforce_detection=False)
        self.Expression_Status = self.Result[0]['dominant_emotion']

    def Process_Frames(self, Frame):
        self.Frame = Frame

        if self.Start_Time == 0:
            self.Start_Time = time.time()

        if(time.time() - self.Start_Time) >= self.Check_Expression_Timer:
            self.Classify()
            self.Start_Time = 0