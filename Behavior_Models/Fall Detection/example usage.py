import Fall_Detection as fd
import cv2
import os

# Send the object of the patient and the model path here        
script_directory = os.path.dirname(os.path.abspath(__file__))

fall = fd.FallDetector(None, script_directory +'/Fall_model2.h5')

# Open the video file (change 'video_file.mp4' to your video file path)
video_file = 'Behavior_Models/Fall Detection/fall.mp4'
cap = cv2.VideoCapture(video_file)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break
    # Call the detection function after reading the frame
    stat, annotated_frame = fall.detect(frame)
    if stat != None:
        cv2.putText(annotated_frame, f'Detection: {stat}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        cv2.imshow("Pose Estimation", annotated_frame)
    else:
        cv2.imshow("Pose Estimation", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit the loop
        break
    # uncomment this line to pause after each frame
    #cv2.waitKey(0)

cap.release()
cv2.destroyAllWindows()

# it may crash when the video ends.