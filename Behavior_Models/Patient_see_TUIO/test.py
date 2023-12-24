from Source import Medicine_TUIO 
import cv2

Object=Medicine_TUIO()

Capture = cv2.VideoCapture(0)

while Capture.isOpened():
    Ret, Frame = Capture.read()
    if not Ret:
        break

    Frame = Frame = cv2.flip(Frame, 1)
    medicines = Object.QRcode_detector(Frame)
    print(medicines)
    cv2.putText(Frame, Object.screen_text, (50, 50), Object.font, Object.font_scale, Object.color, Object.thickness)
    cv2.imshow("TUIO", Frame)

    if (cv2.waitKey(1) & 0xFF == 27):
        break



Capture.release()
cv2.destroyAllWindows()