from tensorflow import keras
import numpy as np
import cv2
import mediapipe as mp
import os

class FallDetector:
    def __init__(self):
        script_directory = os.path.dirname(os.path.abspath(__file__))
        self.stat = "Safe"
        self.model = keras.models.load_model(script_directory +'/Fall_model2.h5')

    def detect(self, frame):

        mp_pose = mp.solutions.pose
        pose = mp_pose.Pose()
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_frame)

        if results.pose_landmarks:
            mp_drawing = mp.solutions.drawing_utils
            annotated_frame = frame.copy()
            mp_drawing.draw_landmarks(
                annotated_frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            
            # Extract the x and y coordinates of the landmarks
            landmark_coords = [[lm.x, lm.y] for lm in results.pose_landmarks.landmark]
            
            # Convert the landmark_coords to a NumPy array
            landmark_coords = np.array(landmark_coords)
            
            # Reshape to match the model's expected input shape (1, 33, 2)
            landmark_coords = landmark_coords.reshape((1, 33, 2))
            
            detection = self.model.predict(landmark_coords)
            self.stat = "Fall" if detection[0] < 0.1 else "Safe"
            print(detection)
            return self.stat, annotated_frame
        return None, frame