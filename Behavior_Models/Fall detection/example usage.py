import Fall_detection as fd
import cv2
from tensorflow import keras

# Send the object of the patient and the model path here        

# Open the video file (change 'video_file.mp4' to your video file path)
video_file = 1
cap = cv2.VideoCapture(video_file)
fall = fd.FallDetector(None, 'Fall_model new.h5')

frame_counter = 0
frame_skip = 2  # Process every 5th frame

stat = "None"
stat_pause = stat
while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break
    # Call the detection function after reading the frame
    if frame_counter % frame_skip != 0:
        frame_counter = 0
        continue
    else:
        stat_pause = stat
    stat, annotated_frame = fall.detect(frame)
    cv2.putText(annotated_frame, 'By: Pola', (500, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    if stat != None:
        cv2.putText(annotated_frame, f'Detection: {stat_pause}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow("Pose Estimation", annotated_frame)
    else:
        cv2.putText(frame, f'Detection: {stat_pause}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow("Pose Estimation", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit the loop
        break
    # uncomment this line to pause after each frame
    #cv2.waitKey(0)
    frame_counter += 1


cap.release()
cv2.destroyAllWindows()

# it may crash when the video ends.
