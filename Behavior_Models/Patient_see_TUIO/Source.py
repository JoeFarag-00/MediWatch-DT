import cv2
import numpy as np
from pyzbar.pyzbar import decode 
import qrcode


class Medicine_TUIO:
    def __init__(self):
        self.num_medicines = 0
        self.cap=cv2.VideoCapture(0)
        self.cap.set(3,640) #for width
        self.cap.set(4,480) #for height
        self.screen_text = "Patient didn't take any medicine"
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.org = (50, 50)
        self.font_scale = 1
        self.color = (255, 255, 255)
        self.thickness = 2

    def generate_qr_codes(self,num_medicines):
        for i in range(num_medicines):
            data = input(f"Enter data for QR code {i + 1}: ")

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )

            qr.add_data(data)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            img.save(f"{data}.png")
            print(f"QR code {i + 1} generated successfully.")
    
    
    def QRcode_detector(self):
        taken_medicines = set()
        all_medicines = set()

        while True:
            success, img = self.cap.read()
            detected_medicines = set()

            for barcode in decode(img):
                my_data = barcode.data.decode('utf-8')
                all_medicines.add(my_data)
                detected_medicines.add(my_data)
                
                data_pts = np.array([barcode.polygon], np.int32)
                data_pts = data_pts.reshape((-1, 1, 2))
                cv2.polylines(img, [data_pts], True, (255, 0, 255), 5)
                word_pts = barcode.rect
                cv2.putText(img, my_data, (word_pts[0], word_pts[1]), cv2.FONT_HERSHEY_DUPLEX,
                            0.9, (255, 0, 255), 2)

            missing_medicines = all_medicines - detected_medicines
            if missing_medicines:
                self.screen_text = f"Patient take: {', '.join(missing_medicines)}"
            

            cv2.putText(img, self.screen_text, (50, 50), self.font, self.font_scale, self.color, self.thickness)
            cv2.imshow('Result', img)
            
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()












# Usage example
tuio=Medicine_TUIO()
num_of_medicines = int(input("Enter the number of medicines: "))
tuio.generate_qr_codes(num_of_medicines)
tuio.QRcode_detector()
