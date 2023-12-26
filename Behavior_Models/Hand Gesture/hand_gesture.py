import mediapipe as mp 
import cv2
from dollarpy import Recognizer, Template, Point
mp_hands=mp.solutions.hands
mp_drawings=mp.solutions.drawing_utils 
mp_styles=mp.solutions.drawing_styles
import pickle
import os

class HandGestureRecognition:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
        self.wrist_points=[]
        self.thumbCMC_points=[]
        self.thumbMCP_points=[]
        self.thumbIP_points=[]
        self.thumbTIP_points=[]
        self.indexfingerMCP_points=[]
        self.indexfingerPIP_points=[]
        self.indexfingerDIP_points=[]
        self.indexfingerTIP_points=[]
        self.middlefingerMCP_points=[]
        self.middlefingerPIP_points=[]
        self.middlefingerDIP_points=[]
        self.middlefingerTIP_points=[]
        self.ringfingerMCP_points=[]
        self.ringfingerPIP_points=[]
        self.ringfingerDIP_points=[]
        self.ringfingerTIP_points=[]
        self.pinkyfingerMCP_points=[]
        self.pinkyfingerPIP_points=[]
        self.pinkyfingerDIP_points=[]
        self.pinkyfingerTIP_points=[]
        self.points=[]
        self.counter=0
        self.script_directory = os.path.dirname(os.path.abspath(__file__))
        self.recognizer = self.load_model(self.script_directory + "/classifier.pkl")

    
    def load_model(self,filename):
        with open(filename, "rb") as f:
            self.recognizer = pickle.load(f)
        return self.recognizer

    def hand_gesture(self,frame):
        bgr = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
        results = self.hands.process(bgr)
        if results.multi_handedness:
            
            for hand_landmarks in results.multi_hand_landmarks:
                for num, hand in enumerate(results.multi_hand_landmarks):
                    mp_drawings.draw_landmarks(frame, hand, mp.solutions.hands.HAND_CONNECTIONS)
                landmarks = []
                for landmark in hand_landmarks.landmark:
                    x = landmark.x
                    y = landmark.y
                    z = landmark.z
                    landmarks.append({"x": x, "y": y, "z": z})
            self.wrist_points.append(Point(landmarks[0]["x"],landmarks[0]["y"],0)) 
            self.thumbCMC_points.append(Point(landmarks[1]["x"],landmarks[1]["y"],1)) 
            self.thumbMCP_points.append(Point(landmarks[2]["x"],landmarks[2]["y"],2)) 
            self.thumbIP_points.append(Point(landmarks[3]["x"],landmarks[3]["y"],3)) 
            self.thumbTIP_points.append(Point(landmarks[4]["x"],landmarks[4]["y"],4)) 
            self.indexfingerMCP_points.append(Point(landmarks[5]["x"],landmarks[5]["y"],5)) 
            self.indexfingerPIP_points.append(Point(landmarks[6]["x"],landmarks[6]["y"],6)) 
            self.indexfingerDIP_points.append(Point(landmarks[7]["x"],landmarks[7]["y"],7)) 
            self.indexfingerTIP_points.append(Point(landmarks[8]["x"],landmarks[8]["y"],8)) 
            self.middlefingerMCP_points.append(Point(landmarks[9]["x"],landmarks[9]["y"],9)) 
            self.middlefingerPIP_points.append(Point(landmarks[10]["x"],landmarks[10]["y"],10)) 
            self.middlefingerDIP_points.append(Point(landmarks[11]["x"],landmarks[11]["y"],11)) 
            self.middlefingerTIP_points.append(Point(landmarks[12]["x"],landmarks[12]["y"],12)) 
            self.ringfingerMCP_points.append(Point(landmarks[13]["x"],landmarks[13]["y"],13)) 
            self.ringfingerPIP_points.append(Point(landmarks[14]["x"],landmarks[14]["y"],14)) 
            self.ringfingerDIP_points.append(Point(landmarks[15]["x"],landmarks[15]["y"],15)) 
            self.ringfingerTIP_points.append(Point(landmarks[16]["x"],landmarks[16]["y"],16)) 
            self.pinkyfingerMCP_points.append(Point(landmarks[17]["x"],landmarks[17]["y"],17)) 
            self.pinkyfingerPIP_points.append(Point(landmarks[18]["x"],landmarks[18]["y"],18)) 
            self.pinkyfingerDIP_points.append(Point(landmarks[19]["x"],landmarks[19]["y"],19)) 
            self.pinkyfingerTIP_points.append(Point(landmarks[20]["x"],landmarks[20]["y"],20)) 
            self.points=self.wrist_points+self.thumbCMC_points+self.thumbMCP_points+self.thumbIP_points+self.thumbTIP_points+self.indexfingerMCP_points+self.indexfingerPIP_points+self.indexfingerDIP_points+self.indexfingerTIP_points+self.middlefingerMCP_points+self.middlefingerPIP_points+self.middlefingerDIP_points+self.middlefingerTIP_points+self.ringfingerMCP_points+self.ringfingerPIP_points+self.ringfingerDIP_points+self.ringfingerTIP_points+self.pinkyfingerMCP_points+self.pinkyfingerPIP_points+self.pinkyfingerDIP_points+self.pinkyfingerTIP_points    
            # print('pts',self.points)
            self.counter+=1
            if(self.counter>10):
                result = self.recognizer.recognize(self.points)
                return result
            else:
                return ["None",1]
        else:
            return ["None",1]