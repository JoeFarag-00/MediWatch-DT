from crud_parent import parent_crud
import copy
from PIL import Image

class Nurse(parent_crud):
    def add_nurse(self, name, DOB, qualifications, department_id, contact_number, gender, floor_number, password, nationality, username, image):
        data = copy.copy(self.nurse_data)
        data["name"] = name
        data["DOB"] = DOB
        data["qualifications"] = qualifications
        data["department_id"] = department_id
        data["contact_number"] = contact_number
        data["floor_number"] = floor_number
        data["gender"] = gender
        data["password"] = password  # Add password for the nurse
        data["nationality"] = nationality
        data["username"] = username
        data["image"] = image
        return self._create(data, self.nurse)
    
    def read_one(self, id=None, name=None, DOB=None, qualifications=None, department_id=None, contact_number=None, gender=None, floor_number=None, password=None, nationality=None, username=None, image=None, filter=None):
        if filter is None:
            filter = self.create_multiple_filter(id, name, DOB, qualifications, department_id, contact_number, gender, floor_number, password, nationality, username, image)
        return self._read_one(filter, self.nurse)
 
    def read_all_nurses(self):
        return self._read_all(self.nurse)

    def create_multiple_filter(self, id=None, name=None, DOB=None, qualifications=None, department_id=None, contact_number=None, gender=None, floor_number=None, password=None, nationality=None, username=None, image=None):
        data = {}
        if id is not None:
            data["_id"] = id
        if name is not None:
            data["name"] = name
        if DOB is not None:
            data["DOB"] = DOB
        if qualifications is not None:
            data["qualifications"] = qualifications
        if department_id is not None:
            data["department_id"] = department_id
        if contact_number is not None:
            data["contact_number"] = contact_number
        if gender is not None:
            data["gender"] = gender
        if floor_number is not None:
            data["floor_number"] = floor_number
        if password is not None:
            data["password"] = password  # Include password in filter criteria
        if nationality is not None:
            data["nationality"] = nationality
        if username is not None:
            data["username"] = username
        if image is not None:
            data["image"] = image
        return data

    def read_all_by_filter(self, id=None, name=None, DOB=None, qualifications=None, department_id=None, contact_number=None, gender=None, floor_number=None, password=None, nationality=None, username=None, image=None, filter=None):
        if filter is None:
            filter = self.create_multiple_filter(id, name, DOB, qualifications, department_id, contact_number, gender, floor_number, password, nationality, username, image)
        all_nurses = self._read_all(self.nurse)
        filtered_nurses = []
        
        for nurse in all_nurses:
            match = True
            for attr, value in filter.items():
                if value is not None and nurse.get(attr) != value:
                    match = False
                    break
            
            if match:
                filtered_nurses.append(nurse)
        
        return filtered_nurses 
    def update_nurse(self, old_data, new_data):
        if set(old_data) != set(new_data):
            print("\n!!!!!!!!!!!!!!!!!!\n!!!!!!!!!!!!!!!!!!\n!!!!!!!The old Data Attr are not the same as the new data!!!!!!\n!!!!!!!!!!!!!!!!!!!!!\n!!!!!!!!!!!!!!!!!!\n")
            return None

        if self.read_one(filter=old_data):
            self._update(old_data, new_data, self.nurse)
            return self.read_one(filter=new_data)

        print("\n!!!!!!!!!!!!!!!!!!\n!!!!!!!!!!!!!!!!!!\n!!!!!!!No user found with the old data to be updated!!!!!!\n!!!!!!!!!!!!!!!!!!!!!\n!!!!!!!!!!!!!!!!!!\n")
        return None




if __name__ == '__main__':
    nurse = Nurse()

    # Add nurse with image
    image_data = open("pola.jpg", "rb")
    image_bytes = image_data.read()
    image_data.close()

    nurse_jane = nurse.add_nurse(
        "Nurse Jane",
        "1990-05-15",
        "RN",
        301,
        "1234567890",
        "Female",
        3,
        "password123",
        "Canada",
        "jane_nurse",
        image=nurse.write_image("pola.jpg")
    )

    # Print nurse with image
    print(nurse_jane)
    print("\n\n\n\n")

    # Add nurse without image
    nurse_john = nurse.add_nurse(
        "Nurse John",
        "1988-07-20",
        "LPN",
        302,
        "9876543210",
        "Male",
        4,
        "securepass",
        "USA",
        "john_nurse",
        image=nurse.write_image("pola.jpg")
    )

    # Print nurse without image
    print(nurse_john)

    # Print all nurses
    nurses = nurse.read_all_nurses()
    print(nurses)
    print("\n\n\n\n")

    # Read one nurse by name
    jane_nurse = nurse.read_one(name="Nurse Jane")
    print(jane_nurse)
    new_im = nurse.display_image(jane_nurse["image"])
    new_im.show()

    print("\n\n\n\n")

    # Read all nurses by department
    john_nurses = nurse.read_all_by_filter(department_id=302)
    print(john_nurses)
    print("\n\n\n\n")

    # Update nurse qualifications
    john_nurse_update = nurse.update_nurse(
        nurse.create_multiple_filter(
            name="Nurse John",
            DOB="1988-07-20",
            qualifications="LPN",
            department_id=302,
            contact_number="9876543210",
            gender="Male",
            floor_number=4
        ),
        nurse.create_multiple_filter(
            name="Nurse John",
            DOB="1988-07-20",
            qualifications="RN",
            department_id=302,
            contact_number="9876543210",
            gender="Male",
            floor_number=4
        )
    )

    # Print updated nurse
    print(john_nurse_update)
    print("\n\n\n\n")

    # Delete nurses
    nurse.delete_nurse(nurse_jane)
    nurse.delete_nurse(john_nurse_update)

    # Print confirmation message
    print("Nurses Jane and John have been deleted.")