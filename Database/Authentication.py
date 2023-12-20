import os
import cv2
import face_recognition
from tkinter import messagebox

script_directory = os.path.dirname(os.path.abspath(__file__))
class FaceIdentificationSystem:

    def __init__(self, nurse_data_path=f"{script_directory}/Faces", known_nurses=None):
        self.nurse_data_path = nurse_data_path
        self.known_nurses = known_nurses or self.load_known_nurses()

    def load_known_nurses(self):
        known_nurses = []
        for nurse_id in os.listdir(self.nurse_data_path):
            nurse_name = "Nurse " + nurse_id
            known_nurses.append({"id": nurse_id, "name": nurse_name})
        return known_nurses

    def start_authentication(self):
        cap = cv2.VideoCapture(1)

        while True:
            ret, frame = cap.read()
            face_locations = face_recognition.face_locations(frame)

            for top, right, bottom, left in face_locations:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            cv2.imshow("Face Authentication", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            if face_locations:
                nurse_id, nurse_name = self.authenticate_face(frame)
                if nurse_id:
                    self.close_camera(cap)
                    return nurse_id, nurse_name

        self.close_camera(cap)

    def authenticate_face(self, frame):
        face_encodings = face_recognition.face_encodings(frame)

        for face_encoding in face_encodings:
            for known_nurse in self.known_nurses:
                known_face_encoding = known_nurse.get("face_encoding")
                if known_face_encoding is None:
                    known_face_encoding = face_recognition.face_encodings(
                        face_recognition.load_image_file(
                            os.path.join(self.nurse_data_path, known_nurse["id"], "1.jpg")
                        )
                    )[0]
                    known_nurse["face_encoding"] = known_face_encoding

                matches = face_recognition.compare_faces([known_face_encoding], face_encoding)

                if matches[0]:
                    return known_nurse["id"], known_nurse["name"]

        return None, None

    def close_camera(self, cap):
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    example_nurses = [
        {"id": "211777", "name": "Youssef"},
        {"id": "212257", "name": "Mina"},
    ]

    face_system = FaceIdentificationSystem(known_nurses=example_nurses)

    result = face_system.start_authentication()

    if result:
        nurse_id, nurse_name = result
        messagebox.showinfo("Authentication Successful", f"Welcome, {nurse_name} (ID: {nurse_id})")
    else:
        messagebox.showwarning("Authentication Failed", "No matching nurse found.")

