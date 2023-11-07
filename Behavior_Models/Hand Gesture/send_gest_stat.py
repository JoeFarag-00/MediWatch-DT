import cv2
import sys
import socket
import time
from hand_gesture import HandGestureRecognition

hand_recognizer = HandGestureRecognition()

cap = cv2.VideoCapture(1)

server_address = ('127.0.0.1', 5000)  
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

while True:
    time.sleep(1)
    ret, frame = cap.read()

    result = hand_recognizer.hand_gesture(frame)
    Status = str(result[0])
    print("Hand Gesture Result:", Status)
    print(type(Status))

    # time.sleep(1)

    if result is not None:
        first_item = result[0]  
        first_item_str = str(first_item)

        result_bytes = first_item_str.encode('utf-8')
        client_socket.sendall(result_bytes)

    cv2.imshow("Hand Gestures", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

client_socket.close()



#None
#fist-hand
#ok