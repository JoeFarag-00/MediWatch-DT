import cv2
import numpy as np 
from pyzbar.pyzbar import decode

cap=cv2.VideoCapture(1)


tui_state = "Awake"


while True:
    
    success, img=cap.read()
    for barcode in decode(img):
        # print(barcode.data)
        myData=barcode.data.decode('utf-8')
        print(myData)
        
        
        if myData == "Green Marker":
            tui_state = "Awake"
        elif myData == "Red Marker":
            tui_state = "Emergency"
    
    cv2.putText(img, f"Current State: {tui_state}", (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    
    
    
    cv2.imshow('Result',img)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()