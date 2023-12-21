from DB_conn import conn
from crud_parent import parent_crud
import copy


class Patient(parent_crud):
    """
    This class is used to create, read, update, and delete patients in the database.

    Methods:
    add_patient(self, name, DOB, disease, room_no, gender, medicines=["Medicine A", "Medicine B"],status = ["safe", "sleeping", "not Eating", "dead"])
        Adds a patient to the database.

    read_all_patients(self)
        Returns a list of all patients in the database.

    read_one(self, id=None, name=None, DOB=None, disease=None, room_no=None, gender=None, medicines=None,status=None, filter=None)
        Returns a single patient from the database based on the specified filter criteria.

    read_all_by_filter(self, id=None, name=None, DOB=None, disease=None, room_no=None, gender=None, medicines=None,status=None, filter = None)
        Returns a list of patients that match the specified filter criteria.

    update_patient(self, old_data, new_data)
        Updates an existing patient in the database.

    delete_patient(self, data)
        Deletes an existing patient from the database.

    """
    def add_patient(self, name, DOB, gender, disease, room_no, medicines, status, password):
        """
        Adds a patient to the database.

        Parameters:
        name (str): The name of the patient.
        DOB (str): The date of birth of the patient.
        gender (str): The gender of the patient.
        disease (str): The disease of the patient.
        room_no (str): The room number of the patient.
        medicines (list): The list of medicines prescribed to the patient.
        status (str): The status of the patient.
        password (str): The password for the patient.

        Returns:
        dict: A dictionary containing the patient information.
        """
        data = copy.copy(self.patient_data)
        data["name"] = name
        data["BOD"] = DOB
        data["gender"] = gender
        data["disease"] = disease
        data["room_no"] = room_no
        data["medicines"] = medicines
        data["status"] = status
        data["password"] = password
        return self._create(data, self.patient)
    
    def create_multiple_filter(self, id=None, name=None, DOB=None, gender=None, disease=None, room_no=None, medicines=None, status=None, password=None):
        """
        Creates a filter based on the specified criteria.

        Parameters:
        id (str, optional): The ID of the patient.
        name (str, optional): The name of the patient.
        DOB (str, optional): The date of birth of the patient.
        gender (str, optional): The gender of the patient.
        disease (str, optional): The disease of the patient.
        room_no (str, optional): The room number of the patient.
        medicines (list, optional): The list of medicines taken by the patient.
        status (str, optional): The status of the patient.
        password (str, optional): The password of the patient.

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
        return data

    def read_all_patients(self):
        """
        Returns a list of all patients in the database.

        Returns:
        list: A list of dictionaries containing the patient information.

        """
        return self._read_all(self.patient)

    def create_multiple_filter(self, id=None, name=None, DOB=None, gender=None, disease=None, room_no=None, medicines=None, status=None, password=None):
        """
        Creates a filter based on the specified criteria.

        Parameters:
        id (str, optional): The ID of the patient.
        name (str, optional): The name of the patient.
        DOB (str, optional): The date of birth of the patient.
        gender (str, optional): The gender of the patient.
        disease (str, optional): The disease of the patient.
        room_no (str, optional): The room number of the patient.
        medicines (list, optional): The list of medicines taken by the patient.
        status (str, optional): The status of the patient.
        password (str, optional): The password of the patient.

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
        return data

    def read_one(self, id=None, name=None, DOB=None, gender=None, disease=None, room_no=None, medicines=None, status=None, password=None, filter=None):
        """
        Returns a single patient based on the specified criteria.

        Parameters:
        id (str, optional): The ID of the patient.
        name (str, optional): The name of the patient.
        DOB (str, optional): The date of birth of the patient.
        gender (str, optional): The gender of the patient.
        disease (str, optional): The disease of the patient.
        room_no (str, optional): The room number of the patient.
        medicines (list, optional): The list of medicines taken by the patient.
        status (str, optional): The status of the patient.
        password (str, optional): The password of the patient.
        filter (dict, optional): A dictionary containing the filter criteria.

        Returns:
        dict: A dictionary containing the patient information.
        """
        if filter is None:
            filter = self.create_multiple_filter(id, name, DOB, gender, disease, room_no, medicines, status, password)
        return self._read_one(filter, self.patient)

    def read_all_by_filter(self, id=None, name=None, DOB=None, gender=None, disease=None, room_no=None, medicines=None, status=None, password=None, filter=None):
        """
        Returns a list of patients that match the specified filter criteria.

        Parameters:
        id (str, optional): The ID of the patient.
        name (str, optional): The name of the patient.
        DOB (str, optional): The date of birth of the patient.
        gender (str, optional): The gender of the patient.
        disease (str, optional): The disease of the patient.
        room_no (str, optional): The room number of the patient.
        medicines (list, optional): The list of medicines taken by the patient.
        status (str, optional): The status of the patient.
        password (str, optional): The password of the patient.
        filter (dict, optional): A dictionary containing the filter criteria.

        Returns:
        list: A list of dictionaries containing the patient information.
        """
        if filter is None:
            filter = self.create_multiple_filter(id, name, DOB, gender, disease, room_no, medicines, status, password)
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
        """
        Updates an existing patient in the database.

        Parameters:
        old_data (dict): The old data of the patient.
        new_data (dict): The new data of the patient.

        Returns:
        dict: A dictionary containing the updated patient information.

        """
        if(set(old_data) != set(new_data)):
            print("\n!!!!!!!!!!!!!!!!!!\n!!!!!!!!!!!!!!!!!!\n!!!!!!!The old Data Attr are not the same as the new data!!!!!!\n!!!!!!!!!!!!!!!!!!!!!\n!!!!!!!!!!!!!!!!!!\n")
            return None

        if self.read_one(filter=old_data):
            self._update(old_data, new_data, self.patient)
            return self.read_one(filter=new_data)
        
        print("\n!!!!!!!!!!!!!!!!!!\n!!!!!!!!!!!!!!!!!!\n!!!!!!!No user found with the old data to be updated!!!!!!\n!!!!!!!!!!!!!!!!!!!!!\n!!!!!!!!!!!!!!!!!!\n")
        return None

    def delete_patient(self, data):
        """
        Deletes an existing patient from the database.

        Parameters:
        data (dict): The data of the patient to be deleted.

        Returns:
        """
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
        "Admitted",#should be an array of stats as pleased
        "password123"
    ))
    print("\n\n\n\n")

    print(patient.add_patient(
        "Alice Smith",
        "1990-05-20",
        "Female",
        "Broken Leg",
        "202B",
        ["Medicine C"],
        "In Treatment", #should be an array of stats as pleased
        "secure_pass"
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
        status="In Treatment",#should be an array of stats as pleased
        password="secure_pass"
    )

    alice_new = patient.create_multiple_filter(
        name="Alice Smith",
        DOB="1990-05-20",
        gender="Female",
        disease="Broken Leg",
        room_no="202B",
        medicines=["Medicine C", "Medicine D"],
        status="Recovered",#should be an array of stats as pleased
        password="secure_pass"
    )

    print(patient.update_patient(alice_old, alice_new))
    print("\n\n\n\n")

    patient.delete_patient(alice_new)
    patient.delete_patient(patient.read_one(name="John Doe"))

    print("\n\n Deleted John Doe and Alice Smith \n\n")
