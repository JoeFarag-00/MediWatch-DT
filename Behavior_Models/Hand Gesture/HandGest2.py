import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import math
from mediapipe.framework.formats import landmark_pb2
import matplotlib.pyplot as plt
import os


class HandGestureProcessor:
    def __init__(self):
        plt.rcParams.update({
            'axes.spines.top': False,
            'axes.spines.right': False,
            'axes.spines.left': False,
            'axes.spines.bottom': False,
            'xtick.labelbottom': False,
            'xtick.bottom': False,
            'ytick.labelleft': False,
            'ytick.left': False,
            'xtick.labeltop': False,
            'xtick.top': False,
            'ytick.labelright': False,
            'ytick.right': False
        })
        
        self.script_directory = os.path.dirname(os.path.abspath(__file__))
        self.path = self.script_directory + '/gesture_recognizer.task'
        self.base_options = python.BaseOptions(model_asset_path=self.path)
        options = vision.GestureRecognizerOptions(base_options=self.base_options)
        self.recognizer = vision.GestureRecognizer.create_from_options(options)
        self.request_status = "idle"

    def process_frame(self, frame):

        frame = cv2.flip(frame, 1)
        image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        recognition_result = self.recognizer.recognize(image)

        if recognition_result.gestures:
            top_gesture = recognition_result.gestures[0][0]
            print(top_gesture)

            # hand_landmarks = recognition_result.hand_landmarks
            results = top_gesture

            if results.category_name == "Open_Palm":
                self.request_status = "Request Made"
            elif results.category_name == "Closed_Fist":
                self.request_status = "Request Canceled"

        # cv2.imshow('Hand Tracking', frame)
        return self.request_status

