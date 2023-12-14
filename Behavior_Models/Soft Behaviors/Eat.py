import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import time
import os

class Eating_Detector:
    def __init__(self):
        self.script_directory = os.path.dirname(os.path.abspath(__file__))

        self.Food_List = ['fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 
                          'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake']
        self.Start_Time = 0
        self.Check_Sleep_Timer = 1
        self.Status_Eating = "Eating"
        self.Status_Not_Eating = "Not Eating"
        self.Flag_Eating = self.Status_Not_Eating

        self.Model_Path = self.script_directory + '\efficientdet.tflite'
        self.Base_Options = python.BaseOptions(model_asset_path = self.Model_Path)
        self.Options = vision.ObjectDetectorOptions(base_options=self.Base_Options, score_threshold=0.1, max_results=10)
        self.Detector = vision.ObjectDetector.create_from_options(self.Options)

    def Draw_Boxes(self):
        for Detection in self.Detection_Result.detections:
            Box_Coordinates = Detection.bounding_box
            Start_Point = Box_Coordinates.origin_x, Box_Coordinates.origin_y
            End_Point = Box_Coordinates.origin_x + Box_Coordinates.width, Box_Coordinates.origin_y + Box_Coordinates.height
            cv2.rectangle(self.Frame_Copy, Start_Point, End_Point, (255, 0, 0), 3)

            Category = Detection.categories[0]
            Category_Name = Category.category_name
            Probability = round(Category.score, 2)
            Result_Text = Category_Name + ' (' + str(Probability) + ')'
            Text_Location = (10 + Box_Coordinates.origin_x, 10 + 10 + Box_Coordinates.origin_y)
            cv2.putText(self.Frame_Copy, Result_Text, Text_Location, cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)

        return self.Frame_Copy

    def Classify(self):
        self.Flag_Eating = self.Status_Not_Eating

        self.Detection_Result = self.Detector.detect(self.Mp_Image)

        for Detection in self.Detection_Result.detections:
            for Category in Detection.categories:
                if Category.category_name in self.Food_List:
                    self.Flag_Eating = self.Status_Eating
                    break
            if self.Flag_Eating == self.Status_Eating:
                break

    def Process_Frames(self, Frame):
        self.Frame = Frame
        self.Mp_Image = mp.Image(image_format = mp.ImageFormat.SRGB, data = self.Frame)

        if self.Start_Time == 0:
            self.Start_Time = time.time()
        
        if(time.time() - self.Start_Time) >= self.Check_Sleep_Timer:
            self.Classify()
            self.Start_Time = 0