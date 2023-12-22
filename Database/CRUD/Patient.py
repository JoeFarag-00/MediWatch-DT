from DB_conn import conn
from crud_parent import parent_crud
import copy


class Patient(parent_crud):

    def add_patient(self, name, DOB, gender, disease, room_no, medicines, status, password, nationality, username, image):
        data = copy.copy(self.patient_data)
        data["name"] = name
        data["DOB"] = DOB
        data["gender"] = gender
        data["disease"] = disease
        data["room_no"] = room_no
        data["medicines"] = medicines
        data["status"] = status
        data["password"] = password
        data["nationality"] = nationality
        data["username"] = username
        data["image"] = image
        return self._create(data, self.patient)

    def create_multiple_filter(self, id=None, name=None, DOB=None, gender=None, disease=None, room_no=None, medicines=None, status=None, password=None, nationality=None, username=None, image=None):
        data = {}
        if id is not None:
            data["_id"] = id
        if name is not None:
            data["name"] = name
        if DOB is not None:
            data["DOB"] = DOB
        if gender is not None:
            data["gender"] = gender
        if disease is not None:
            data["disease"] = disease
        if room_no is not None:
            data["room_no"] = room_no
        if medicines is not None:
            data["medicines"] = medicines
        if status is not None:
            data["status"] = status
        if password is not None:
            data["password"] = password  # Include password in filter criteria
        if nationality is not None:
            data["nationality"] = nationality
        if username is not None:
            data["username"] = username
        if image is not None:
            data["image"] = image
        return data

    def read_all_patients(self):
        return self._read_all(self.patient)

    def create_multiple_filter(self, id=None, name=None, DOB=None, gender=None, disease=None, room_no=None, medicines=None, status=None, password=None, nationality=None, username=None, image=None):
        data = {}
        if id is not None:
            data["_id"] = id
        if name is not None:
            data["name"] = name
        if DOB is not None:
            data["DOB"] = DOB
        if gender is not None:
            data["gender"] = gender
        if disease is not None:
            data["disease"] = disease
        if room_no is not None:
            data["room_no"] = room_no
        if medicines is not None:
            data["medicines"] = medicines
        if status is not None:
            data["status"] = status
        if password is not None:
            data["password"] = password  # Include password in filter criteria
        if nationality is not None:
            data["nationality"] = nationality
        if username is not None:
            data["username"] = username
        if image is not None:
            data["image"] = image
        return data

    def read_one(self, id=None, name=None, DOB=None, gender=None, disease=None, room_no=None, medicines=None, status=None, password=None, nationality=None, username=None, filter=None, image=None):
        if filter is None:
            filter = self.create_multiple_filter(id, name, DOB, gender, disease, room_no, medicines, status, password, nationality, username, image)
        return self._read_one(filter, self.patient)

    def read_all_by_filter(self, id=None, name=None, DOB=None, gender=None, disease=None, room_no=None, medicines=None, status=None, password=None, nationality=None, username=None, filter=None, image=None):
        if filter is None:
            filter = self.create_multiple_filter(id, name, DOB, gender, disease, room_no, medicines, status, password, nationality, username, image)
        all_patients = self._read_all(self.patient)
        filtered_patients = []

        for patient in all_patients:
            match = True
            for attr, value in filter.items():
                if value is not None and patient.get(attr) != value:
                    match = False
                    break

            if match:
                filtered_patients.append(patient)

        return filtered_patients

    def update_patient(self, old_data, new_data):
        if (set(old_data) != set(new_data)):
            print("\n!!!!!!!!!!!!!!!!!!\n!!!!!!!!!!!!!!!!!!\n!!!!!!!The old Data Attr are not the same as the new data!!!!!!\n!!!!!!!!!!!!!!!!!!!!!\n!!!!!!!!!!!!!!!!!!\n")
            return None

        if self.read_one(filter=old_data):
            self._update(old_data, new_data, self.patient)
            return self.read_one(filter=new_data)

        print("\n!!!!!!!!!!!!!!!!!!\n!!!!!!!!!!!!!!!!!!\n!!!!!!!No user found with the old data to be updated!!!!!!\n!!!!!!!!!!!!!!!!!!!!!\n!!!!!!!!!!!!!!!!!!\n")
        return None

    def delete_patient(self, data):
        self._delete(data, self.patient)


if __name__ == '__main__':
    patient = Patient()

    print(patient.add_patient(
        "John Doe",
        "1985-07-15",
        "Male",
        "Fever",
        "101A",
        ["Medicine A", "Medicine B"],
        "Admitted",  # should be an array of stats as pleased
        "password123",
        "American",
        "jdoe",
        "https://example.com/johndoe.jpg"
    ))
    print("\n\n\n\n")

    print(patient.add_patient(
        "Alice Smith",
        "1990-05-20",
        "Female",
        "Broken Leg",
        "202B",
        ["Medicine C"],
        "In Treatment",  # should be an array of stats as pleased
        "secure_pass",
        "British",
        "alice_smith",
        "https://example.com/alicesmith.jpg"
    ))

    print(patient.read_all_patients())
    print("\n\n\n\n")

    print(patient.read_one(name="John Doe"))
    print("\n\n\n\n")

    print(patient.read_all_by_filter(disease="Broken Leg"))
    print("\n\n\n\n")

    alice_old = patient.create_multiple_filter(
        name="Alice Smith",
        DOB="1990-05-20",
        gender="Female",
        disease="Broken Leg",
        room_no="202B",
        medicines=["Medicine C"],
        status="In Treatment",  # should be an array of stats as pleased
        password="secure_pass",
        nationality="British",
        username="alice_smith",
        image="https://example.com/alicesmith.jpg"
    )

    alice_new = patient.create_multiple_filter(
        name="Alice Smith",
        DOB="1990-05-20",
        gender="Female",
        disease="Broken Leg",
        room_no="202B",
        medicines=["Medicine C", "Medicine D"],
        status="Recovered",  # should be an array of stats as pleased
        password="secure_pass",
        nationality="American",
        username="alice_smith",
        image="https://example.com/alicesmith_recovered.jpg"
    )

    print(patient.update_patient(alice_old, alice_new))
    print("\n\n\n\n")

    patient.delete_patient(alice_new)
    patient.delete_patient(patient.read_one(name="John Doe"))

    print("\n\n Deleted John Doe and Alice Smith \n\n")
