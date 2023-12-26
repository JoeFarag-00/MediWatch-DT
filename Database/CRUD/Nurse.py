from crud_parent import parent_crud
import copy

class Nurse(parent_crud):
    """
    This class is used to create, read, update, and delete nurses in the database.

    Methods:
    add_nurse(self, name, DOB, qualifications, department_id, contact_number, gender, floor_number)
        Adds a nurse to the database.
    
    """
    def add_nurse(self, name, DOB, qualifications, department_id, contact_number, gender, floor_number, password):
        """
        Adds a nurse to the database.

        Parameters:
        name (str): The name of the nurse.
        DOB (str): The date of birth of the nurse.
        qualifications (str): The qualifications of the nurse.
        department_id (int): The department ID of the nurse.
        contact_number (str): The contact number of the nurse.
        gender (str): The gender of the nurse.
        floor_number (int): The floor number where the nurse is located.
        password (str): The password of the nurse.

        Returns:
        dict: A dictionary containing the nurse information.
        """
        data = copy.copy(self.nurse_data)
        data["name"] = name
        data["BOD"] = DOB
        data["qualifications"] = qualifications
        data["department_id"] = department_id
        data["contact_number"] = contact_number
        data["floor_number"] = floor_number
        data["gender"] = gender
        data["password"] = password  # Add password for the nurse
        return self._create(data, self.nurse)
    
    def read_one(self, id=None, name=None, DOB=None, qualifications=None, department_id=None, contact_number=None, gender=None, floor_number=None, password=None, filter=None):
        """
        Returns a single nurse based on the specified criteria.

        Parameters:
        id (str, optional): The ID of the nurse.
        name (str, optional): The name of the nurse.
        DOB (str, optional): The date of birth of the nurse.
        qualifications (str, optional): The qualifications of the nurse.
        department_id (int, optional): The department ID of the nurse.
        contact_number (str, optional): The contact number of the nurse.
        gender (str, optional): The gender of the nurse.
        floor_number (int, optional): The floor number where the nurse is located.
        password (str, optional): The password of the nurse.
        filter (dict, optional): A dictionary containing the filter criteria.

        Returns:
        dict: A dictionary containing the nurse information.
        """
        if filter is None:
            filter = self.create_multiple_filter(id, name, DOB, qualifications, department_id, contact_number, gender, floor_number, password)
        return self._read_one(filter, self.nurse)
 
    def read_all_nurses(self):
        """
        Returns a list of all nurses in the database.

        Returns:
        list: A list of dictionaries containing the nurse information.
        """
        return self._read_all(self.nurse)

    def create_multiple_filter(self, id=None, name=None, DOB=None, qualifications=None, department_id=None, contact_number=None, gender=None, floor_number=None, password=None):
        """
        Creates a filter based on the specified criteria.

        Parameters:
        id (str, optional): The ID of the nurse.
        name (str, optional): The name of the nurse.
        DOB (str, optional): The date of birth of the nurse.
        qualifications (str, optional): The qualifications of the nurse.
        department_id (int, optional): The department ID of the nurse.
        contact_number (str, optional): The contact number of the nurse.
        gender (str, optional): The gender of the nurse.
        floor_number (int, optional): The floor number where the nurse is located.
        password (str, optional): The password of the nurse.

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
        if password is not None:
            data["password"] = password  # Include password in filter criteria
        return data

    def read_all_by_filter(self, id=None, name=None, DOB=None, qualifications=None, department_id=None, contact_number=None, gender=None, floor_number=None, password=None, filter=None):
        """
        Returns a list of nurses that match the specified filter criteria.

        Parameters:
        id (str, optional): The ID of the nurse.
        name (str, optional): The name of the nurse.
        DOB (str, optional): The date of birth of the nurse.
        qualifications (str, optional): The qualifications of the nurse.
        department_id (int, optional): The department ID of the nurse.
        contact_number (str, optional): The contact number of the nurse.
        gender (str, optional): The gender of the nurse.
        floor_number (int, optional): The floor number where the nurse is located.
        password (str, optional): The password of the nurse.
        filter (dict, optional): A dictionary containing the filter criteria.

        Returns:
        list: A list of dictionaries containing the nurse information.
        """
        if filter is None:
            filter = self.create_multiple_filter(id, name, DOB, qualifications, department_id, contact_number, gender, floor_number, password)
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
        """
        Updates an existing nurse in the database.

        Parameters:
        old_data (dict): The old data of the nurse.
        new_data (dict): The new data of the nurse.

        Returns:
        dict: A dictionary containing the updated nurse information.
        """
        if set(old_data) != set(new_data):
            print("\n!!!!!!!!!!!!!!!!!!\n!!!!!!!!!!!!!!!!!!\n!!!!!!!The old Data Attr are not the same as the new data!!!!!!\n!!!!!!!!!!!!!!!!!!!!!\n!!!!!!!!!!!!!!!!!!\n")
            return None

        if self.read_one(filter=old_data):
            self._update(old_data, new_data, self.nurse)
            return self.read_one(filter=new_data)

        print("\n!!!!!!!!!!!!!!!!!!\n!!!!!!!!!!!!!!!!!!\n!!!!!!!No user found with the old data to be updated!!!!!!\n!!!!!!!!!!!!!!!!!!!!!\n!!!!!!!!!!!!!!!!!!\n")
        return None

    def delete_nurse(self, data):
        """
        Deletes an existing nurse from the database.

        Parameters:
        data (dict): The data of the nurse to be deleted.

        Returns:
        """
        self._delete(data, self.nurse)



if __name__ == '__main__':
    nurse = Nurse()

    print(nurse.add_nurse(
        "Nurse Jane",
        "1990-05-15",
        "RN",
        301,
        "1234567890",
        "Female",
        3,
        "password123"  # Include nurse password
    ))
    print("\n\n\n\n")

    print(nurse.add_nurse(
        "Nurse John",
        "1988-07-20",
        "LPN",
        302,
        "9876543210",
        "Male",
        4,
        "securepass"  # Include nurse password
    ))

    print(nurse.read_all_nurses())
    print("\n\n\n\n")

    print(nurse.read_one(name="Nurse Jane"))
    print("\n\n\n\n")

    print(nurse.read_all_by_filter(department_id=302))
    print("\n\n\n\n")

    nurse_john_old = nurse.create_multiple_filter(
        name="Nurse John",
        DOB="1988-07-20",
        qualifications="LPN",
        department_id=302,
        contact_number="9876543210",
        gender="Male",
        floor_number=4
    )

    nurse_john_new = nurse.create_multiple_filter(
        name="Nurse John",
        DOB="1988-07-20",
        qualifications="RN",
        department_id=302,
        contact_number="9876543210",
        gender="Male",
        floor_number=4
    )

    print(nurse.update_nurse(nurse_john_old, nurse_john_new))
    print("\n\n\n\n")

    nurse.delete_nurse(nurse_john_new)
    nurse.delete_nurse(nurse.read_one(name="Nurse Jane"))

    print("\n\n Deleted Nurse John and Nurse Jane \n\n")