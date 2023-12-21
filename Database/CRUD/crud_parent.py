from DB_conn import conn
class parent_crud:
    """
    This class is used to create, read, update, and delete data in the database.
    """
    def __init__(self):
        """
        Initialize the class by connecting to the database.
        """
        self.db = conn()
        self.patient = 'patient'
        self.nurse = 'nurse'
        self.doctor = 'doctor'

        self.patient_data = {
            "name":           None,
            "BOD":            None,
            "gender":         None,
            "disease":        None,
            "room_no":        None,
            "medicines":      None,
            "status":         None,
            "password":       None
        }

        self.doctor_data = {
            "name":           None,
            "BOD":            None,
            "gender":         None,
            "qualifications": None,
            "department_id":  None,
            "contact_number": None,
            "floor_number":   None,
            "nurses_in_help": None,
            "password":       None
        }

        self.nurse_data = {
            "name":           None,
            "BOD":            None,
            "gender":         None,
            "qualifications": None,
            "department_id":  None,
            "contact_number": None,
            "floor_number":   None,
            "password":       None
        }


    def _create(self, data, type):
        """
        Create a new record in the database.
        This function is not made for calling outside the this class
        Args:
            data (dict): The data to be inserted into the database.
            type (str): The collection name.

        Returns:
            pymongo.results.InsertOneResult: The result of the insert operation.
        """
        return self.db[type].insert_one(data)

    def _read_all(self, type):
        """
        Read all records from the database.
        This function is not made for calling outside the this class
        Args:
            type (str): The collection name.

        Returns:
            list: A list of all records in the collection.
        """
        return list(self.db[type].find())

    def _read_one(self, data, type):
        """
        Read a single record from the database.
        This function is not made for calling outside the this class
        Args:
            data (dict): The query to match against.
            type (str): The collection name.

        Returns:
            dict: The matching record, or None if no match is found.
        """
        return self.db[type].find_one(data)

    def _update(self, old_data, new_data, type):
        """
        Update an existing record in the database.
        This function is not made for calling outside the this class
        Args:
            old_data (dict): The query to match against.
            new_data (dict): The data to be updated.
            type (str): The collection name.

        Returns:
            dict: The updated record.
        """
        self.db[type].replace_one(old_data, new_data)
        return self._read_one(new_data, type)

    def _delete(self, data, type):
        """
        Delete an existing record from the database.
        This function is not made for calling outside the this class
        Args:
            data (dict): The query to match against.
            type (str): The collection name.
        """
        self.db[type].delete_one(data)

if __name__ == '__main__':
    # Usage example:
    dataset = parent_crud()
    data = {
        "name": "Powder",
        "BOD": "1813-01-01",
        "gender": "Male",
        "qualifications": "Registered Nurse",
        "department_id": 103,
        "contact_number": "23456190",
        "floor_number": 3
    }

    new_data = {
        "name": "Youssef",
        "BOD": "1813-01-01",
        "gender": "Male",
        "qualifications": "Registered Nurse",
        "department_id": 103,
        "contact_number": "23456190",
        "floor_number": 3
    }

    print(dataset._create(data, dataset.nurse))
    print("\n\npowder has been created successfully.\n\n")
    print(dataset._read_all(dataset.nurse))
    print("\n\n")
    print(f"\n\npowder has been updated successfully.{dataset._update(data, new_data, dataset.nurse)}\n\n")
    print("\n\n")
    print(dataset._read_all(dataset.nurse))
    print("\n\n")
    dataset._delete(new_data, dataset.nurse)
    print("\n\npowder has been deleted successfully.\n\n")
    print(f"powder data: {dataset._read_one(new_data, dataset.nurse)}")
