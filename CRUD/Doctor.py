from DB_conn import conn
from crud_parent import parent_crud
import copy

class Doctor(parent_crud):
    """
    This class is used to create, read, update, and delete doctors in the database.

    Methods:
    add_doctor(self, name, DOB, qualifications, department_id, contact_number, gender, floor_number, no_nurses_in_help)
        Adds a doctor to the database.
    
    """

    def add_doctor(self, name, DOB, qualifications, department_id, contact_number, gender, floor_number, no_nurses_in_help, password):
        """
        Adds a doctor to the database.

        Parameters:
        name (str): The name of the doctor.
        DOB (str): The date of birth of the doctor.
        qualifications (str): The qualifications of the doctor.
        department_id (int): The department ID of the doctor.
        contact_number (str): The contact number of the doctor.
        gender (str): The gender of the doctor.
        floor_number (int): The floor number where the doctor is located.
        no_nurses_in_help (int): Number of nurses the doctor is associated with.
        password (str): The password of the doctor.

        Returns:
        dict: A dictionary containing the doctor information.

        """
        data = copy.copy(self.doctor_data)
        data["name"] = name
        data["BOD"] = DOB
        data["qualifications"] = qualifications
        data["department_id"] = department_id
        data["contact_number"] = contact_number
        data["floor_number"] = floor_number
        data["nurses_in_help"] = no_nurses_in_help
        data["gender"] = gender
        data["password"] = password
        return self._create(data, self.doctor)

    def read_all_doctors(self):
        """
        Returns a list of all doctors in the database.

        Returns:
        list: A list of dictionaries containing the doctor information.

        """
        return self._read_all(self.doctor)

    def create_multiple_filter(self, id=None, name=None, DOB=None, qualifications=None, department_id=None, contact_number=None, gender=None, floor_number=None, nurses_in_help=None, password=None):
        """
        Creates a filter based on the specified criteria.

        Parameters:
        id (str, optional): The ID of the doctor.
        name (str, optional): The name of the doctor.
        DOB (str, optional): The date of birth of the doctor.
        qualifications (str, optional): The qualifications of the doctor.
        department_id (int, optional): The department ID of the doctor.
        contact_number (str, optional): The contact number of the doctor.
        gender (str, optional): The gender of the doctor.
        floor_number (int, optional): The floor number where the doctor is located.
        no_nurses_in_help (int, optional): Number of nurses the doctor is associated with.
        password (str, optional): The password of the doctor.

        Returns:
        dict: A dictionary containing the filter criteria.

        """
        data = {}
        if id is not None:
            data["_id"] = id
        if name is not None:
            data["name"] = name
        if DOB is not None:
            data["BOD"] = DOB
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
        if nurses_in_help is not None:
            data["nurses_in_help"] = nurses_in_help
        if password is not None:
            data["password"] = password
        return data

    def read_one(self, id=None, name=None, DOB=None, qualifications=None, department_id=None, contact_number=None, gender=None, floor_number=None, no_nurses_in_help=None, password=None, filter=None):
        if filter is None:
            filter = self.create_multiple_filter(id, name, DOB, qualifications, department_id, contact_number, gender, floor_number, no_nurses_in_help, password)
        return self._read_one(filter, self.doctor)

    def read_all_by_filter(self, id=None, name=None, DOB=None, qualifications=None, department_id=None, contact_number=None, gender=None, floor_number=None, no_nurses_in_help=None, password=None, filter=None):
        """
        Returns a list of doctors that match the specified filter criteria.

        Parameters:
        id (str, optional): The ID of the doctor.
        name (str, optional): The name of the doctor.
        DOB (str, optional): The date of birth of the doctor.
        qualifications (str, optional): The qualifications of the doctor.
        department_id (int, optional): The department ID of the doctor.
        contact_number (str, optional): The contact number of the doctor.
        gender (str, optional): The gender of the doctor.
        floor_number (int, optional): The floor number where the doctor is located.
        no_nurses_in_help (int, optional): Number of nurses the doctor is associated with.
        password (str, optional): The password of the doctor.

        Returns:
        list: A list of dictionaries containing the doctor information.

        """
        if filter is None:
            filter = self.create_multiple_filter(id, name, DOB, qualifications, department_id, contact_number, gender, floor_number, no_nurses_in_help, password)
        all_doctors = self._read_all(self.doctor)
        filtered_doctors = []
        
        for doctor in all_doctors:
            match = True
            for attr, value in filter.items():
                if value is not None and doctor.get(attr) != value:
                    match = False
                    break
            
            if match:
                filtered_doctors.append(doctor)
        
        return filtered_doctors
    def update_doctor(self, old_data, new_data):
            """
            Updates an existing doctor in the database.

            Parameters:
            old_data (dict): The old data of the doctor.
            new_data (dict): The new data of the doctor.

            Returns:
            dict: A dictionary containing the updated doctor information.
            """
            if set(old_data) != set(new_data):
                print("\n!!!!!!!!!!!!!!!!!!\n!!!!!!!!!!!!!!!!!!\n!!!!!!!The old Data Attr are not the same as the new data!!!!!!\n!!!!!!!!!!!!!!!!!!!!!\n!!!!!!!!!!!!!!!!!!\n")
                return None

            if self.read_one(filter=old_data):
                self._update(old_data, new_data, self.doctor)
                return self.read_one(filter=new_data)

            print("\n!!!!!!!!!!!!!!!!!!\n!!!!!!!!!!!!!!!!!!\n!!!!!!!No user found with the old data to be updated!!!!!!\n!!!!!!!!!!!!!!!!!!!!!\n!!!!!!!!!!!!!!!!!!\n")
            return None

    def delete_doctor(self, data):
        """
        Deletes an existing doctor from the database.

        Parameters:
        data (dict): The data of the doctor to be deleted.

        Returns:
        """
        self._delete(data, self.doctor)


if __name__ == '__main__':
    doctor = Doctor()

    print(doctor.add_doctor(
        "Dr. Smith",
        "1978-05-20",
        "MD",
        202,
        "9876543210",
        "Female",
        5,
        ["Nurse 1", "Nurse 2"],
        "password123"  # Add password when creating a doctor
    ))
    print("\n\n\n\n")

    print(doctor.add_doctor(
        "Dr. Johnson",
        "1980-08-10",
        "MD",
        201,
        "9876543210",
        "Male",
        6,
        ["Nurse 3", "Nurse 4"],
        "securepass"  # Add password when creating a doctor
    ))

    print(doctor.read_all_doctors())
    print("\n\n\n\n")

    print(doctor.read_one(name="Dr. Smith"))
    print("\n\n\n\n")

    print(doctor.read_all_by_filter(department_id=201))
    print("\n\n\n\n")

    dr_johnson_old = doctor.create_multiple_filter(
        name="Dr. Johnson",
        DOB="1980-08-10",
        qualifications="MD",
        department_id=201,
        contact_number="9876543210",
        gender="Male",
        floor_number=6,
        nurses_in_help=["Nurse 3", "Nurse 4"],
        password="securepass"  # Include password in the filter
    )

    dr_johnson_new = doctor.create_multiple_filter(
        name="Dr. Johnson",
        DOB="1980-08-10",
        qualifications="PhD",
        department_id=201,
        contact_number="9876543210",
        gender="Male",
        floor_number=6,
        nurses_in_help=["Nurse 3", "Nurse 4"],
        password="securepass"  # Include password in the filter
    )

    print(doctor.update_doctor(dr_johnson_old, dr_johnson_new))
    print("\n\n\n\n")

    doctor.delete_doctor(dr_johnson_new)
    doctor.delete_doctor(doctor.read_one(name="Dr. Smith"))

    print("\n\n Deleted Dr. Johnson and Dr. Smith \n\n")
