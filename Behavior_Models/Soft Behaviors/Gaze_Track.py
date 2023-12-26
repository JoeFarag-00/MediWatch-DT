import cv2
import numpy as np
import mediapipe as mp
import csv
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

class Gaze_Tracking:
    def __init__(self, Path = ""):
        self.Path = Path
        self.Average_Eye_X = 0
        self.Average_Eye_Y = 0
        self.Left_Center = 0
        self.Right_Center = 0

        self.Script_Directory = os.path.dirname(os.path.abspath(__file__))
        CSV_Filename = "Gaze_Data.csv"
        self.CSV_Path = self.Script_Directory + f"\{CSV_Filename}"
        self.CSV_File = open(self.CSV_Path, mode='w', newline='')
        self.CSV_Writer = csv.writer(self.CSV_File)

        if len(self.Path) > 0:
            self.Capture = cv2.VideoCapture(self.Path)
        else:
            self.Capture = cv2.VideoCapture(0)

        self.Mp_FaceMesh = mp.solutions.face_mesh
        self.Face_Mesh = self.Mp_FaceMesh.FaceMesh(max_num_faces = 1, refine_landmarks = True, min_detection_confidence=0.5, min_tracking_confidence = 0.5)

        self.Mp_Drawing = mp.solutions.drawing_utils

        self.Left_Eye_LM = [ 362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385,384, 398 ]
        self.Right_Eye_LM = [ 33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161 , 246 ] 
        self.Left_Iris = [469, 470, 471, 472]
        self.Right_Iris = [474, 475, 476, 477]

    def Draw_Iris(self):

        # cv2.polylines(self.Frame, [self.Coordinates[self.Left_Iris]], True, (0, 255, 0), 1, cv2.LINE_AA)
        # cv2.polylines(self.Frame, [self.Coordinates[self.Right_Iris]], True, (0, 255, 0), 1, cv2.LINE_AA)

        cv2.circle(self.Frame, self.Left_Center, int(1), (0, 255, 0), 1, cv2.LINE_AA)
        cv2.circle(self.Frame, self.Right_Center, int(1), (0, 255, 0), 1, cv2.LINE_AA)

        # cv2.putText(self.Frame, f"{self.Left_Center}, {self.Right_Center}", (20, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

        return self.Frame
    
    def Generate_Heatmap(self):
        Eye_Data = pd.read_csv(self.CSV_Path, header=None,names=["X","Y"])
        fig,ax=plt.subplots(figsize=(10,8))
        sns.kdeplot(x=Eye_Data['X'],y=Eye_Data['Y'],fill=True,
                    cmap='rainbow', cbar=False,alpha=0.4)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_frame_on(False)
        plt.savefig(self.Script_Directory + "\Heatmap.png",bbox_inches='tight',pad_inches=0)

    def Process_Frames(self, Frame):
        self.Frame = Frame

        self.Frame = cv2.cvtColor(self.Frame, cv2.COLOR_BGR2RGB)
        self.Frame.flags.writeable = False

        self.Results = self.Face_Mesh.process(self.Frame)
        
        self.Frame.flags.writeable = True
        self.Frame = cv2.cvtColor(self.Frame, cv2.COLOR_RGB2BGR)

        self.Height, self.Width, self.Channels = self.Frame.shape

        
        if self.Results.multi_face_landmarks:
            for self.Face_Land_Marks in self.Results.multi_face_landmarks:

                self.Average_Eye_X = (self.Face_Land_Marks.landmark[self.Left_Iris[1]].x + self.Face_Land_Marks.landmark[self.Right_Iris[1]].x) / 2
                self.Average_Eye_Y = (self.Face_Land_Marks.landmark[self.Left_Iris[1]].y + self.Face_Land_Marks.landmark[self.Right_Iris[1]].y) / 2
                self.CSV_Writer.writerow([self.Average_Eye_X, self.Average_Eye_Y])
                self.CSV_File.flush()
                self.Coordinates = np.array([np.multiply([Point.x,Point.y], [self.Width, self.Height]).astype(int) for Point in self.Face_Land_Marks.landmark])
                
                (self.Left_x, self.Left_y), self.Left_Radius = cv2.minEnclosingCircle(self.Coordinates[self.Left_Iris])
                (self.Right_x, self.Right_y), self.Right_Radius = cv2.minEnclosingCircle(self.Coordinates[self.Right_Iris])

                self.Left_Center = np.array([self.Left_x, self.Left_y], dtype = np.int32)
                self.Right_Center = np.array([self.Right_x, self.Right_y], dtype = np.int32)
        else:
            self.Average_Eye_X
            self.Average_Eye_Y 