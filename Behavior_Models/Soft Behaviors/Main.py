from Soft_Behavior_Detector import *

Object = Soft_Behavior_Detector()

Capture = cv2.VideoCapture(0)

while Capture.isOpened():
    Ret, Frame = Capture.read()
    if not Ret:
        break
    
    Frame = Frame = cv2.flip(Frame, 1)
    
    Object.Classify(Frame)


    # print(Object.Expression_Status, Object.Flag_Eating, Object.Flag_Sleeping)
    # Frame = Object.Sleep.Drawy_Eye()
    cv2.putText(Frame, f"{Object.Expression_Status}, {Object.Flag_Eating}, {Object.Flag_Sleeping}", (20, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
    cv2.putText(Frame, f"{Object.Eye_X_Frame_Coordinate}, {Object.Eye_Y_Frame_Coordinate}", (20, 70), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
    if Object.Sleep.Start_Time > 0:
        cv2.putText(Frame, Object.Sleep.Timer, (20, 110), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
    cv2.imshow("Soft Behavior Classification", Frame)
    
    if (cv2.waitKey(1) & 0xFF == 27 or cv2.getWindowProperty("Soft Behavior Classification", cv2.WND_PROP_VISIBLE) < 1):
        break

Capture.release()
cv2.destroyAllWindows()