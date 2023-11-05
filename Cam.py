import cv2

Cam1 = cv2.VideoCapture(1)
Cam2 = cv2.VideoCapture(2)

while True:
    ret1, frame1 = Cam1.read()
    ret2, frame2 = Cam2.read()

    cv2.imshow('Camera 1', frame1)
    cv2.imshow('Camera 2', frame2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

Cam1.release()
Cam2.release()
#Pola Sign-IN
cv2.destroyAllWindows()
