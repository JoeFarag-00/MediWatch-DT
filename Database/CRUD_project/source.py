from dotenv import load_dotenv,find_dotenv
import os
import pprint
from pymongo import MongoClient
from bson.objectid import ObjectId
import io
from PIL import Image
load_dotenv(find_dotenv())

password=os.environ.get("MONGODB_PWD")



connection_string=f"mongodb+srv://steven:{password}@cluster0.pfzxzcu.mongodb.net/?retryWrites=true&w=majority"

client=MongoClient(connection_string)



dbs=client.list_database_names()
print("the databases names we have ", dbs)


elder_people_dbs=client.elder_people_system
collections=elder_people_dbs.list_collection_names()
print('these are the collections we have in our database',collections)



class Patient:
    def __init__(self):
        self.printer = pprint.PrettyPrinter()
        self.patient_collection=elder_people_dbs.patient
    
    def create_patient_doc(self,name, age, disease, room_no, medicines, gender,Nationality,Priority_Care,Medical_Desc,image):
        patient_document = {
            "name": name,
            "age": age,
            "disease": disease,
            "room_no": room_no,
            "medicines": medicines,
            "gender": gender,
            "Nationality":Nationality,
            "Priority_Care":Priority_Care,
            "Medical_Desc":Medical_Desc,
            "image":image
        }
        patient_inserted_id = self.patient_collection.insert_one(patient_document).inserted_id
        print("The patient document number ", patient_inserted_id)
    
    def create_patients_docs(self,patients_list):
        inserted_ids = []
        for patient_details in patients_list:
            patient_document = {
                "name": patient_details.get("name", ""),                                      
                "age": patient_details.get("age", 0),
                "disease": patient_details.get("disease", ""),
                "room_no": patient_details.get("room_no", ""),
                "medicines": patient_details.get("medicines", []),
                "gender": patient_details.get("gender", ""),
                "Nationality":patient_details.get("Nationality",""),
                "Priority_Care":patient_details.get("Priority_Care",""),
                "Medical_Desc":patient_details.get("Medical_Desc",""),
                "image":patient_details.get("image",),
            }
            patient_inserted_id = self.patient_collection.insert_one(patient_document).inserted_id
            inserted_ids.append(patient_inserted_id)
        print("The patient document numbers:", inserted_ids)
    
    # Read
    def read_all_patients(self):
        patients=self.patient_collection.find()
        return(list(patients))
    
    def read_specific_patient_by_name(self,name):
        patient = self.patient_collection.find_one({"name": name})
        return patient
    
    def count_all_patient_with_filter(self,filter=None):
        patient_count = self.patient_collection.count_documents(filter)
        # print('Patient number:', patient_count)
        return patient_count
    
    def get_patient_by_id(self,person_id):
        patient_id=ObjectId(person_id)
        patient=self.patient_collection.find_one({"_id":patient_id})
        return patient
    
    def get_patient_age_range(self,min_age,max_age):
    
        query={
                "$and":[
                    {"age":{"$gte":min_age}},
                    {"age":{"$lte":max_age}},
                ]
            }
        patients=self.patient_collection.find(query).sort("age")
        return patients
    
    def specific_patients_cols(self, include_fields=None, exclude_fields=None):
        columns = set()

        if include_fields:
            columns.update(include_fields)

        if exclude_fields:
            columns.difference_update(exclude_fields)

        patients = self.patient_collection.find({}, columns)
        
        # Extracting columns only
        extracted_columns = [{key: patient[key] for key in columns if key in patient} for patient in patients]
        
        return extracted_columns

    # update
    def update_patient_by_id(self,patient_id, set_fields=None, unset_fields=None):
        patient_id = ObjectId(patient_id)
        update_query = {}

        if set_fields:
            set_updates = {f"$set": set_fields}
            update_query.update(set_updates)

        if unset_fields:
            unset_updates = {f"$unset": unset_fields}
            update_query.update(unset_updates)

        if update_query:
            self.patient_collection.update_one({"_id": patient_id}, update_query)
    
    def replace_one_patient_doc(self,id, new_patient_document):
        patient_id = ObjectId(id)
        self.patient_collection.replace_one({"_id": patient_id}, new_patient_document)
    
    
    # Delete
    def delete_patient_doc_by_field(self,field, value):
        self.patient_collection.delete_one({field: value})
        
    # image handling
    def display_image(self, image_bytes):
        # Load the image from the image bytes
        image = Image.open(io.BytesIO(image_bytes))
        return image
    
    def write_image(self, path):
        with open(path, 'rb') as image_file:
            image_bytes = image_file.read()
        return image_bytes
    









# Testing for patient class 
steven=Patient()
# steven.create_patient_doc("mina", 21, "Anger", "D112", ["ketofan", "dalflon"], "female","egyptian","high","can kill himself",
#                         steven.write_image("Cristiano Ronaldo.jpeg"))







patients = [
    {
        "name": "Steven",
        "age": 21,
        "disease": "Anger",
        "room_no": "D112",
        "medicines": ["ketofan", "dalflon"],
        "gender": "male"
    },
    {
        "name": "Alice",
        "age": 30,
        "disease": "Fever",
        "room_no": "C301",
        "medicines": ["paracetamol", "ibuprofen"],
        "gender": "female"
    }
]
# steven.create_patients_docs(patients)

# patients=steven.read_all_patients()
# print(patients)



# patient_name = "mina"
# patient = steven.read_specific_patient_by_name(patient_name)
# print(patient)
# steven.display_image(patient["image"]).show()


# disease_filter = {"disease": "Fever"}
# patient_count=steven.count_all_patient_with_filter(filter=disease_filter)
# print(patient_count)

# patient_by_id= steven.get_patient_by_id("6569da4d4068ea61c75dacf5")
# print(patient_by_id)


# patients=steven.get_patient_age_range(10,40)
# for patient in patients:
#     steven.printer.pprint(patient)


# cols=steven.specific_patients_cols(include_fields=["age", "name"])
# print(cols)


# steven.update_patient_by_id("6569daad0e00ba3817b56d22", set_fields={"diabetes": False, "age": 25})
# steven.update_patient_by_id("6569daad0e00ba3817b56d22", unset_fields={"diabetes": "", "age": ""})


new_patient = {
    "name": "4am3oon",
    "age": 10,
    "disease": "idiot",
    "room_no": "D111",
    "medicines": ["medicine 1", "another medicine"],
    "gender": "female"
}

# steven.replace_one_patient_doc("6569daad0e00ba3817b56d21", new_patient)


# steven.delete_patient_doc_by_field("name", "4am3oon")






# nurse class 

class Nurse:
    def __init__(self):
        self.printer = pprint.PrettyPrinter()
        self.nurse_collection=elder_people_dbs.nurse
    
    def create_nurse_doc(self, name, age, qualifications, department_id, contact_number, gender,floor_number,image):
        nurse_document = {
            "name": name,
            "age": age,
            "qualifications": qualifications,
            "department_id": department_id,
            "contact_number": contact_number,
            "gender": gender,
            "floor_number":floor_number,
            "image":image,
        }
        nurse_inserted_id = self.nurse_collection.insert_one(nurse_document).inserted_id
        print("The nurse document number ", nurse_inserted_id)
    
    def create_nurses_docs(self,nurses_list):
        inserted_ids = []
        for nurse_details in nurses_list:
            nurse_document = {
                "name": nurse_details.get("name", ""),
                "age": nurse_details.get("age", 0),
                "qualifications": nurse_details.get("qualifications", ""),
                "department_id": nurse_details.get("department_id", ""),
                "contact_number": nurse_details.get("contact_number", ""),
                "gender": nurse_details.get("gender", ""),
                "floor_number": nurse_details.get("floor_number", 0),
                "image":nurse_details.get("image",)
            }
            nurse_inserted_id = self.nurse_collection.insert_one(nurse_document).inserted_id
            inserted_ids.append(nurse_inserted_id)
        print("The nurse document numbers:", inserted_ids)
    
    # Read
    def read_all_nurses(self):
        nurses=self.nurse_collection.find()
        return(list(nurses))
    
    def read_specific_nurse_by_name(self,name):
        nurse = self.nurse_collection.find_one({"name": name})
        return nurse
    
    def count_all_nurse_with_filter(self,filter=None):
        nurse_count = self.nurse_collection.count_documents(filter)
        # print('nurse number:', nurse_count)
        return nurse_count
    
    def get_nurse_by_id(self,person_id):
        nurse_id=ObjectId(person_id)
        nurse=self.nurse_collection.find_one({"_id":nurse_id})
        return nurse

    def get_nurse_age_range(self,min_age,max_age):
    
        query={
                "$and":[
                    {"age":{"$gte":min_age}},
                    {"age":{"$lte":max_age}},
                ]
            }
        nurses=self.nurse_collection.find(query).sort("age")
        return nurses

    def specific_nurses_cols(self, include_fields=None, exclude_fields=None):
        columns = set()

        if include_fields:
            columns.update(include_fields)

        if exclude_fields:
            columns.difference_update(exclude_fields)

        nurses = self.nurse_collection.find({}, columns)
        
        # Extracting columns only
        extracted_columns = [{key: nurse[key] for key in columns if key in nurse} for nurse in nurses]
        
        return extracted_columns
    
    # update
    def update_nurse_by_id(self,nurse_id, set_fields=None, unset_fields=None):
        nurse_id = ObjectId(nurse_id)
        update_query = {}

        if set_fields:
            set_updates = {f"$set": set_fields}
            update_query.update(set_updates)

        if unset_fields:
            unset_updates = {f"$unset": unset_fields}
            update_query.update(unset_updates)

        if update_query:
            self.nurse_collection.update_one({"_id": nurse_id}, update_query)
    
    def replace_one_nurse_doc(self,id, new_nurse_document):
        nurse_id = ObjectId(id)
        self.nurse_collection.replace_one({"_id": nurse_id}, new_nurse_document)
    
    
    # Delete
    def delete_nurse_doc_by_field(self,field, value):
        self.nurse_collection.delete_one({field: value})
    
    def display_image(self, image_bytes):
        # Load the image from the image bytes
        image = Image.open(io.BytesIO(image_bytes))
        return image
    
    def write_image(self, path):
        with open(path, 'rb') as image_file:
            image_bytes = image_file.read()
        return image_bytes





# testing the nurse class

# steven=Nurse()


# Creating a nurse document using the test data
# steven.create_nurse_doc("pola",30,"RN,BSN" ,"Nursing Department","123-456-7890","Female",2)





nurses = [
    {
        "name": "youssef",
        "age": 21,
        "qualifications": "RN,BSN",
        "department_id": "Nursing Department_5",
        "contact_number": "121-746-8788",  
        "gender": "female",
        "floor_number": 10
    },
    {
        "name": "mina",
        "age": 21,
        "qualifications": "RN,BSN",
        "department_id": "Nursing Department_2",
        "contact_number": "121-546-8788",  
        "gender": "female",
        "floor_number": 1
    }
]
# steven.create_nurses_docs(nurses)


# nurses=steven.read_all_nurses()
# print(nurses)



# nurse_name = "pola"
# nurse = steven.read_specific_nurse_by_name(nurse_name)
# print(nurse)


# gender_filter = {"gender": "female"}
# nurse_count=steven.count_all_nurse_with_filter(filter=gender_filter)
# print(nurse_count)


# nurse_by_id= steven.get_nurse_by_id("65718ea40f95e6c30a2955bc")
# print(nurse_by_id)


# nurses=steven.get_nurse_age_range(10,40)
# for nurse in nurses:
#     steven.printer.pprint(nurse)




# cols=steven.specific_nurses_cols(include_fields=["age", "name"])
# print(cols)



# steven.update_nurse_by_id("65718ea40f95e6c30a2955bc", set_fields={"patients_under_supervision": 12, "age": 25})
# steven.update_nurse_by_id("65718ea40f95e6c30a2955bc", unset_fields={"qualifications": ""})




new_nurse = {
    "name": "4am3oon",
    "age": 10,
    "qualifications": "RN,BSN",
    "flooar_no": "10",
    "department_id": "Nursing_department_5",
    "gender": "male"
}

# steven.replace_one_nurse_doc("6574b7bfa818f15d6ba7be5f", new_nurse)


# steven.delete_nurse_doc_by_field("name", "4am3oon")


# end of Nurse testing
printer = pprint.PrettyPrinter()

# Doctor class 

class Doctor:
    def __init__(self):
        self.printer = pprint.PrettyPrinter()
        self.doctor_collection=elder_people_dbs.doctor
    
    def create_doctor_doc(self, name, age, qualifications, department_id, contact_number, gender,floor_number,no_nurses_in_help,image):
        doctor_document = {
            "name": name,
            "age": age,
            "qualifications": qualifications,
            "department_id": department_id,
            "contact_number": contact_number,
            "gender": gender,
            "floor_number":floor_number,
            "no_nurses_in_help":no_nurses_in_help,
            "image":image,
        }
        doctor_inserted_id = self.doctor_collection.insert_one(doctor_document).inserted_id
        print("The doctor document number ", doctor_inserted_id)

    def create_doctors_docs(self,doctors_list):
        inserted_ids = []
        for doctor_details in doctors_list:
            doctor_document = {
                "name": doctor_details.get("name", ""),
                "age": doctor_details.get("age", 0),
                "qualifications": doctor_details.get("qualifications", ""),
                "department_id": doctor_details.get("department_id", ""),
                "contact_number": doctor_details.get("contact_number", ""),
                "gender": doctor_details.get("gender", ""),
                "floor_number": doctor_details.get("floor_number", 0),
                "no_nurses_in_help": doctor_details.get("no_nurses_in_help", 0),
                "image":doctor_details.get("image",)
            }
            doctor_inserted_id = self.doctor_collection.insert_one(doctor_document).inserted_id
            inserted_ids.append(doctor_inserted_id)
        print("The doctor document numbers:", inserted_ids)
    
    # Read
    def read_all_doctors(self):
        doctors=self.doctor_collection.find()
        return(list(doctors))
    
    def read_specific_doctor_by_name(self,name):
        doctor = self.doctor_collection.find_one({"name": name})
        return doctor
    
    def count_all_doctor_with_filter(self,filter=None):
        doctor_count = self.doctor_collection.count_documents(filter)
        # print('doctor number:', doctor_count)
        return doctor_count
    
    def get_doctor_by_id(self,person_id):
        doctor_id=ObjectId(person_id)
        doctor=self.doctor_collection.find_one({"_id":doctor_id})
        return doctor

    def get_doctor_age_range(self,min_age,max_age):
    
        query={
                "$and":[
                    {"age":{"$gte":min_age}},
                    {"age":{"$lte":max_age}},
                ]
            }
        doctors=self.doctor_collection.find(query).sort("age")
        return doctors

    def specific_doctors_cols(self, include_fields=None, exclude_fields=None):
        columns = set()

        if include_fields:
            columns.update(include_fields)

        if exclude_fields:
            columns.difference_update(exclude_fields)

        doctors = self.doctor_collection.find({}, columns)
        
        # Extracting columns only
        extracted_columns = [{key: doctor[key] for key in columns if key in doctor} for doctor in doctors]
        
        return extracted_columns
    
    # update
    def update_doctor_by_id(self,doctor_id, set_fields=None, unset_fields=None):
        doctor_id = ObjectId(doctor_id)
        update_query = {}

        if set_fields:
            set_updates = {f"$set": set_fields}
            update_query.update(set_updates)

        if unset_fields:
            unset_updates = {f"$unset": unset_fields}
            update_query.update(unset_updates)

        if update_query:
            self.doctor_collection.update_one({"_id": doctor_id}, update_query)
    
    def replace_one_doctor_doc(self,id, new_doctor_document):
        doctor_id = ObjectId(id)
        self.doctor_collection.replace_one({"_id": doctor_id}, new_doctor_document)
    
    
    # Delete
    def delete_doctor_doc_by_field(self,field, value):
        self.doctor_collection.delete_one({field: value})
    
    def display_image(self, image_bytes):
        # Load the image from the image bytes
        image = Image.open(io.BytesIO(image_bytes))
        return image
    
    def write_image(self, path):
        with open(path, 'rb') as image_file:
            image_bytes = image_file.read()
        return image_bytes
    
    





# testing the Doctor class

steven=Doctor()
#  "name": name,
#             "age": age,
#             "qualifications": qualifications,
#             "department_id": department_id,
#             "contact_number": contact_number,
#             "gender": gender,
#             "floor_number":floor_number,
#             "no_nurses_in_help":no_nurses_in_help,
#             "image":image,

# Creating a nurse document using the test data
# steven.create_doctor_doc("pola",30,"RN,BSN" ,"Nursing Department","123-456-7890","Female",2,5,steven.write_image("Cristiano Ronaldo.jpeg"))


doctors = [
    {
        "name": "samo",
        "age": 21,
        "qualifications": "RN,BSN",
        "department_id": "diabetties Department_5",
        "contact_number": "121-746-8788",  
        "gender": "female",
        "floor_number": 10,
        "no_nurses_in_help": 3
    },
    {
        "name": "mina",
        "age": 21,
        "qualifications": "RN,BSN",
        "department_id": "diabetties Department_2",
        "contact_number": "121-546-8788",  
        "gender": "female",
        "floor_number": 1,
        "no_nurses_in_help": 2
    }
]
# steven.create_doctors_docs(doctors)



# doctors=steven.read_all_doctors()
# printer.pprint(doctors)


# doctor_name = "pola"
# doctor = steven.read_specific_doctor_by_name(doctor_name)
# printer.pprint(doctor)


# gender_filter = {"gender": "female"}
# doctor_count=steven.count_all_doctor_with_filter(filter=gender_filter)
# print(doctor_count)


# doctor_by_id= steven.get_doctor_by_id("6575ad14ccd55c196d35b52a")
# printer.pprint(doctor_by_id)


# doctors=steven.get_doctor_age_range(10,40)
# for doctor in doctors:
#     steven.printer.pprint(doctor)


# cols=steven.specific_doctors_cols(include_fields=["age", "name"])
# print(cols)


# steven.update_doctor_by_id("6575ad14ccd55c196d35b52a", set_fields={"patients_under_supervision": 12, "age": 25})
# steven.update_doctor_by_id("6575ad14ccd55c196d35b52a", unset_fields={"qualifications": ""})


new_doctor = {
    "name": "4am3oon",
    "age": 10,
    "qualifications": "RN,BSN",
    "flooar_no": "10",
    "department_id": "Nursing_department_5",
    "gender": "male"
}

# steven.replace_one_doctor_doc("6575ae3b9295b7f0b4faa569", new_doctor)


# steven.delete_doctor_doc_by_field("name", "4am3oon")




# the end of the CRUD by Steven Hany:)