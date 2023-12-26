from Patient import Patient

# Create an instance of the Patient class
patient_instance = Patient()

# View all recorded patients
all_patients = patient_instance.read_all_patients()

# Print patient information
for patient in all_patients:
    print("Patient ID:", patient["_id"])
    print("Name:", patient["name"])
    print("Date of Birth:", patient["BOD"])
    print("Gender:", patient["gender"])
    print("Disease:", patient["disease"])
    print("Room Number:", patient["room_no"])
    print("Medicines:", patient["medicines"])
    print("Status:", patient["status"])
    print("Password:", patient["password"])
    print("\n")
