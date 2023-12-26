import cv2
import numpy as np
import mediapipe as mp
import time
from scipy.spatial import distance

class Sleeping_Detector:
    def __init__(self):
        self.Mp_FaceMesh = mp.solutions.face_mesh
        self.Face_Mesh = self.Mp_FaceMesh.FaceMesh(max_num_faces = 1, refine_landmarks = True, min_detection_confidence=0.5, min_tracking_confidence = 0.5)

        self.Mp_Drawing = mp.solutions.drawing_utils

        self.Ratio_Threshold = 6
        self.Start_Time = 0
        self.Status_Sleep = "Sleeping"
        self.Status_Awake = "Awake"
        self.Flag_Sleep = self.Status_Awake
        self.Check_Sleep_Timer = 20
        self.Left_Eye_LM = [ 362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385,384, 398 ]
        self.Right_Eye_LM = [ 33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161 , 246 ] 
    
    def Draw_Face_Mesh(self):
        for Face_Land_Marks in self.Results.multi_face_landmarks:
            #FACEMESH_CONTOURS, FACEMESH_TESSELATION
            self.Mp_Drawing.draw_landmarks(self.Frame, Face_Land_Marks, self.Mp_FaceMesh.FACEMESH_TESSELATION)
    
    def Drawy_Eye(self):
        cv2.polylines(self.Frame, [self.Coordinates[self.Left_Eye_LM]], True, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.polylines(self.Frame, [self.Coordinates[self.Right_Eye_LM]], True, (0, 255, 0), 1, cv2.LINE_AA)

        return self.Frame

    def Calculate_Ratio(self):
        RHorizontal_Right = self.Coordinates[self.Right_Eye_LM[0]]
        RHorizontal_Left = self.Coordinates[self.Right_Eye_LM[8]]
        RVertical_UP = self.Coordinates[self.Right_Eye_LM[12]]
        RVertical_Down = self.Coordinates[self.Right_Eye_LM[4]] 

        LHorizontal_Right = self.Coordinates[self.Left_Eye_LM[0]]
        LHorizontal_Left = self.Coordinates[self.Left_Eye_LM[8]]
        LVertical_UP = self.Coordinates[self.Left_Eye_LM[12]]
        LVertical_Down = self.Coordinates[self.Left_Eye_LM[4]]

        RHorizontalDistance = distance.euclidean(RHorizontal_Right, RHorizontal_Left)
        RVerticalDistance = distance.euclidean(RVertical_UP, RVertical_Down)
        
        LVerticalDistance = distance.euclidean(LVertical_UP, LVertical_Down)
        LHorizontalDistance = distance.euclidean(LHorizontal_Right, LHorizontal_Left)

        if RVerticalDistance != 0 and LVerticalDistance != 0:
            RightRatio = RHorizontalDistance/RVerticalDistance
            LeftRatio = LHorizontalDistance/LVerticalDistance
            Ratio = (RightRatio+LeftRatio)/2
        else:
            Ratio = 10
        
        return Ratio

    def Process_Frames(self, Frame):
        self.Frame = Frame

        self.Frame = cv2.cvtColor(self.Frame, cv2.COLOR_BGR2RGB)
        self.Frame.flags.writeable = False

        self.Results = self.Face_Mesh.process(self.Frame)
        
        self.Frame.flags.writeable = True
        self.Frame = cv2.cvtColor(self.Frame, cv2.COLOR_RGB2BGR)

        if self.Results.multi_face_landmarks:
            for self.Face_Land_Marks in self.Results.multi_face_landmarks:
                self.Height, self.Width, self.Channels = self.Frame.shape

                self.Coordinates = np.array([np.multiply([Point.x,Point.y], [self.Width, self.Height]).astype(int) for Point in self.Face_Land_Marks.landmark])

                self.Ratio = self.Calculate_Ratio()
                
                if self.Ratio >= self.Ratio_Threshold and self.Start_Time == 0:
                    self.Start_Time = time.time()
                elif self.Ratio < self.Ratio_Threshold:
                    self.Start_Time = 0

                if self.Start_Time > 0:
                    self.Timer = str(round(time.time() - self.Start_Time, 2)) + "/20"

                if self.Ratio > self.Ratio_Threshold and (time.time() - self.Start_Time) >= self.Check_Sleep_Timer:
                    self.Flag_Sleep = self.Status_Sleep
                else:
                    self.Flag_Sleep = self.Status_Awake