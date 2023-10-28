#Fall detection script - output FALL STATUS

import cv2

def process_frame(frame):
    # Your fall detection code here
    # For this example, we'll also display the frames in a window.
    cv2.imshow('Fall Detection', frame)
    cv2.waitKey(1)  # Keep the window open to display the frames
