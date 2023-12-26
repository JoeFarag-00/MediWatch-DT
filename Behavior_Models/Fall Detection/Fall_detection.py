from tensorflow import keras
import numpy as np
import cv2
import mediapipe as mp

class FallDetector:
    def __init__(self):
        '''
        This class must receive a patient object to continue and model path.
        For now send it with any thing.
        Also the pirority it should be in the patient object as a function which determines the priority of the patient.
        '''
        self.patient = ""
        self.stat = "Safe"
        self.model = keras.models.load_model("Behavior_Models\Fall Detection\Fall_model new.h5")

    def detect(self, frame):
        '''
        This function receives a frame and returns the stat ("Safe", "Fall", "None") note: None is not a string and returns the annotated frame.
        For each frame a further calculation is needed to determine if it is a real fall or not.
        like if he is sleeping it is okay, also if it detects a Fall for like 15 frame you should say it is a fall. 
        This calculation will be implmented later.
        '''
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
            self.stat = "Fall" if detection[0] < 0.5 else "Safe"
            
            print(detection)
            pose.close()
            return self.stat
        pose.close()
        return "Safe"
