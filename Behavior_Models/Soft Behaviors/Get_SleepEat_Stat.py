import cv2
# sys.path.append('Behavior_Models/Soft Behaviors')
from Soft_Behavior_Detector import Soft_Behavior_Detector
Get_Soft_Stat = Soft_Behavior_Detector()
cap = cv2.VideoCapture(1)


while cap.isOpened():
    # time.sleep(1)
    Ret, Frame = cap.read()
    if not Ret:
        break
    Get_Soft_Stat.Classify(Frame)
    Sleep_Stat = Get_Soft_Stat.Flag_Sleeping
    Eating_Stat = Get_Soft_Stat.Flag_Eating
    print(f"{Sleep_Stat}, {Eating_Stat}")
    Frame = Get_Soft_Stat.Sleep.Frame
    cv2.putText(Frame, str(Eating_Stat), (200, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
    cv2.imshow('Soft Behavior', Frame)

    if (cv2.waitKey(1) & 0xFF == 27 or cv2.getWindowProperty("Soft Behavior", cv2.WND_PROP_VISIBLE) < 1):
        break

cap.release()
cv2.destroyAllWindows()