import customtkinter
import os
import threading
from datetime import datetime
import tkinter
from tkinter import simpledialog
from tkinter import messagebox
from tkinter import filedialog
customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('green')
import re
import cv2
from tkinter import Label, Text, Button, Menu
import random
from PIL import Image
from tkinter_webcam import webcam
import time
from pymongo import MongoClient
import sys
import pycountry
import socket
from shutil import copyfile
sys.path.append('Behavior_Models/Fall Detection')
from Fall_detection import FallDetector

sys.path.append('Behavior_Models/Soft Behaviors')
from Soft_Behavior_Detector import Soft_Behavior_Detector
sys.path.append('Behavior_Models/Hand Gesture')
from HandGest2 import HandGestureProcessor
sys.path.append('Database')
from Authentication import FaceIdentificationSystem
# sys.path.append("Behavior_Models/TUIO")
# from Source import Medicine_TUIO

sys.path.append('Database')
from source import Patient
from source import Nurse




Main = customtkinter.CTk()

class MainGUI:
    def __init__(self):
        self.Main = Main
        self.start_model = False
        self.Load_Stats = False
        self.Patient_DB = None

        self.IsAddedPatient = False
        self.Patient_Frames_List = []
        self.Nurse_Frames_List = []
        
        self.PushRow = None
        self.PushCol = None
        
        self.Patients_Data_Card = [
            {"name": "Youssef Mohamed", "age": 20, "room_number": "G103A", "disease": "Flu", "image_path": "me.jpg"},
            {"name": "Mina Samir", "age": 21, "room_number": "G408A", "disease": "Alzheimer's", "image_path": "mina.jpg"},
            {"name": "Steven Hany", "age": 21, "room_number": "D101", "disease": "Anger", "image_path": "steven.jpg"},
            {"name": "Pola Emanuel", "age": 21, "room_number": "E205", "disease": "Rheumatoid", "image_path": "pola2.jpg"},
        ]
        self.Nurse_Data_Card = [
            {"name": "Abdo Moota", "age": 47, "qualifications": "Doctor", "department_id": "D122","contact_number": "01024985562","gender":"Male","floor_number":3 ,"image_path": "Abdo.png"},
            {"name": "Hamada Hamdoon ", "age": 26,"qualifications": "EMT", "department_id": "A132", "contact_number": "01553309309","gender":"Male","floor_number":3 ,"image_path": "Hamada.png"},
            {"name": "Sabrina Sabarny", "age": 30, "qualifications": "Nurse", "department_id": "D126", "contact_number": "0103668966","gender":"Female","floor_number":2 ,"image_path": "Sabrina.png"},
            {"name": "Samantha Rohantha", "age": 27, "qualifications": "Nurse", "department_id": "G1252", "contact_number": "0102984552","gender":"Female","floor_number":1 ,"image_path": "Samantha.png"},
        ]
        self.medlist = []
        self.Patient_Labels = []
        self.Information_List = ["Patient Name: ", "DOB: ", "Gender: ", "Nationality: ", "Complication: ", "Priority Care: ", "Room Number: ", "Medicines: " ,"Medical Description: "]
        
        self.Nurses = [
        {"id": "211777", "password": "1234","name": "Youssef"},
        {"id": "212257", "password": "1234","name": "Mina"},
        ]
        
        self.Get_Gest_Stat = HandGestureProcessor()
        self.Get_Soft_Stat = Soft_Behavior_Detector()
        self.Get_Fall_Stat = FallDetector()
        self.Face_System = FaceIdentificationSystem(known_nurses=self.Nurses)
        self.Patient_DB = Patient()
        self.Nurse_DB = Nurse()
        # self.MediTUIO =Medicine_TUIO()
        
        self.image_path = None

    @staticmethod
    def DestroyAll():
        widgets = Main.winfo_children()
        for widget in widgets:
            widget.destroy()

    def Exit(self):
        os._exit(0)


    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def Get_Dashboard(self):
        self.DestroyAll()
        self.bots = None
        self.users = None
        self.sent_message = None
        self.received_message = None
        self.Gesture_Stat = None
        self.message_counter = 1
        self.chat_counter = 2
        self.Main.resizable(width=False, height=False)
        self.Main.title("Dashboard")
        self.Main.geometry(f"{1100}x{510}")
        self.Main.grid_columnconfigure(1, weight=1)
        self.app_logo = customtkinter.CTkImage(light_image=Image.open("Assets/doctor.png"), size=(100, 100))
        self.sidebar_frame = customtkinter.CTkFrame(self.Main, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo = customtkinter.CTkLabel(self.sidebar_frame, image=self.app_logo, text="", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Nurse", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=1, column=0, padx=20)
        
        self.Profile_Button = customtkinter.CTkButton(self.sidebar_frame, text="Profile")
        self.Profile_Button.grid(row=2, column=0, padx=20, pady=10)
        
        self.Settings_Button = customtkinter.CTkButton(self.sidebar_frame, text="Settings")
        self.Settings_Button.grid(row=4, column=0, padx=20, pady=10)
        
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_options = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_options.grid(row=5, column=0, padx=20, pady=(15))
        self.exit_button = customtkinter.CTkButton(self.sidebar_frame, text="Exit", hover_color="Red", command=self.Exit)
        self.exit_button.grid(row=6, column=0, padx=20, pady=15)
        self.tabview = customtkinter.CTkTabview(master=self.Main, width=250, height=490)
        self.tabview.grid(row=1, column=1, columnspan=2, padx=(20, 10), pady=(10, 0), sticky="nsew")
        self.tabview.add("View Patients")
        self.tabview.set("View Patients")
        self.tabview.add("Register Patients")
        self.tabview.add("Active Nurses")
        self.set_name()
        self.Register_Patients()
        self.Apply_Patient_Profiles()
        self.Nurse_Availability()

    def Nurse_Availability(self):
        self.scrollable_frame2 = customtkinter.CTkScrollableFrame(self.tabview.tab("Active Nurses"), width=845,height=430)
        self.scrollable_frame2.grid(row=0, column=0, padx=(5, 0), pady=(5, 0), sticky="nsew")
        self.scrollable_frame2.grid_columnconfigure(0, weight=1)

        self.current_path = os.path.dirname(os.path.realpath(__file__))
        
        max_columns = 3

        for ipx, Nurse_Data in enumerate(self.Nurse_Data_Card):
            row_index = ipx // max_columns
            col_index = ipx % max_columns

            self.nurse_frame = customtkinter.CTkFrame(self.scrollable_frame2, corner_radius=20, fg_color="#628680", border_width=5, border_color="black", width=250, height=300)
            self.nurse_frame.grid(row=row_index, column=col_index, padx=10, pady=15)
            self.Nurse_Frames_List.append(self.nurse_frame)

            image_path = os.path.join(self.current_path, f"Database/Nurse/{Nurse_Data['image_path']}")
            Nurse_Image = customtkinter.CTkImage(Image.open(image_path), size=(200, 250))
            self.Nurse_image_label = customtkinter.CTkLabel(self.nurse_frame, image=Nurse_Image, text="")
            self.Nurse_image_label.grid(row=0, column=0, padx=10, pady=(15, 15))

            nurse_description = f"Name: {Nurse_Data['name']}\n\nAge: {Nurse_Data['age']}\n\nQualifications: {Nurse_Data['qualifications']}\n\nDep ID: {Nurse_Data['department_id']}\n\nContact Number: {Nurse_Data['contact_number']}"
            print(nurse_description)
            self.Nurse_description_label = customtkinter.CTkLabel(self.nurse_frame, text=nurse_description, text_color="white", font=("System", 22, "bold"))
            self.Nurse_description_label.grid(row=1, column=0, padx=10, pady=(15, 15))
    
    def Check_Name(self):
        Name = self.First_Name_Entry.get() + self.Last_Name_Entry.get()
        return not any(char.isdigit() for char in Name)
    
    def Check_Ints(self,input_string):
        return input_string.isdigit()

    def get_DOB(self):
        try:
            Date = self.Dob_day_Entry.get() + "/" + self.Dob_month_Entry.get() + "/" + self.Dob_year_Entry.get()
            dob_date = datetime.strptime(Date, "%d/%m/%Y")
            current_date = datetime.now()
            age = current_date.year - dob_date.year - ((current_date.month, current_date.day) < (dob_date.month, dob_date.day))
            return age
        except ValueError as e:
            print("Error in Calculating Age: ", e)
        
    def get_countries(self):
        country_names_unsorted = [country.name for country in pycountry.countries]
        country_names = sorted(country_names_unsorted)
        return country_names

    def Get_Patient_Pic(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")])
        
        if self.image_path:
            self.Patient_img = customtkinter.CTkImage(Image.open(self.image_path),size=(210, 250))
            self.Patientimg_Label = customtkinter.CTkLabel(self.LoadImg_Frame, image=self.Patient_img,text = "")
            self.Patientimg_Label.grid(row=0, column=0, padx=20, pady=(20, 20))
    
            
    def Store_Patient(self):
        self.WarningLabel = customtkinter.CTkLabel(Main, text="Missing Fields...", font=customtkinter.CTkFont(size=20, weight="bold"),text_color="red" )
        if self.image_path and self.First_Name_Entry.get() and self.Last_Name_Entry.get() and self.Dob_day_Entry.get() and self.Dob_month_Entry.get() and self.Dob_year_Entry.get() and self.Gender_Btn.get() and self.country_box.get() and self.Disease_Entry.get() and self.Priority_Btn.get() and self.Medical_Description_TBOX.get('0.0','end'):
            if self.image_path:
                if self.Check_Name:
                    if self.Check_Ints(self.Dob_day_Entry.get()) and self.Check_Ints(self.Dob_month_Entry.get()) and self.Check_Ints(self.Dob_year_Entry.get()):
    
                        destination_folder = "Database/Patients" 
                        file_name = os.path.basename(self.image_path)
                        destination_path = os.path.join(destination_folder, file_name)
                        try:
                            copyfile(self.image_path, destination_path)
                            print(f"Image '{file_name}' successfully copied to '{destination_folder}'")
                        except Exception as e:
                            print(f"Error copying image: {e}")
                            
                        Name = self.First_Name_Entry.get()+" "+self.Last_Name_Entry.get()
                        Age = self.get_DOB()
                        Disease = self.Disease_Entry.get()
                        Room = self.Room_Number.get()
                        medlist = [obj.strip() for obj in self.Medicine.get().split(',')]
                        gender = self.Gender_Btn.get()
                        nationality = self.country_box.get()
                        Priority_Care = self.Priority_Btn.get()
                        Medical_Desc = self.Medical_Description_TBOX.get('0.0','end')
                        image = self.Patient_DB.write_image(self.image_path)
                        self.Patient_DB.create_patient_doc(Name, Age, Disease, Room, medlist, gender, nationality,Priority_Care,Medical_Desc,image)
                        
                        print(f"Patient Name:{self.First_Name_Entry.get()+' '+self.Last_Name_Entry.get()}\n",
                            f"DOB: {self.Dob_day_Entry.get() + '/' + self.Dob_month_Entry.get() + '/' + self.Dob_year_Entry.get()}\n", 
                            f"Age: {self.get_DOB()}\n",
                            f"Gender: {self.Gender_Btn.get()}\n", 
                            f"Nationality: {self.country_box.get()}\n", 
                            f"Complication: {self.Disease_Entry.get()}\n",
                            f"Priority Care: {self.Priority_Btn.get()}\n",
                            f"Room: {self.Room_Number.get()}"
                            f"Medical Description: {self.Medical_Description_TBOX.get('0.0','end')}\n")
                        
                        new_patient = {"name": Name, "age": Age, "room_number": Room, "disease": Disease, "image_path": file_name}
                        self.Patients_Data_Card.append(new_patient)
                        # print("DATABASE",self.Patients_Data_Card)
                    
                        self.Apply_Patient_Profiles()
                        
                        self.WarningLabel.destroy()
                    else:
                        messagebox.showerror("Invalid Date Entry","Please Enter a Valid Date")   
                else:
                    messagebox.showerror("Invalid Entry","Please Enter a Valid Name.")
            else:
                messagebox.showerror("Missing Image","Please Choose an Image")
        else:
            messagebox.showerror("Missing Fields","Please populate missing fields")
            
    def Register_Patients(self):
 
        self.Patient_Picture_Frame = customtkinter.CTkFrame(self.tabview.tab("Register Patients"), width=550,height=430)
        self.Patient_Picture_Frame.grid(row=0, column=0, padx=(30, 20), pady=(10, 10))
        
        self.LoadImg_Frame = customtkinter.CTkFrame(self.Patient_Picture_Frame, corner_radius=20, fg_color="#628680",border_width=5, border_color="black",width=250,height=300)
        self.LoadImg_Frame.grid(row=0, column=0,pady=(30,20))

        self.Load_Image_Btn = customtkinter.CTkButton(self.Patient_Picture_Frame, text="Load Image",width=200, font=("System", 30, "bold"), fg_color="#628680", command=lambda:self.Get_Patient_Pic())
        self.Load_Image_Btn.grid(row=1, column=0,pady=20)
        
        
        self.scrollable_frame2 = customtkinter.CTkScrollableFrame(self.tabview.tab("Register Patients"), width=550,height=430)
        self.scrollable_frame2.grid(row=0, column=1, padx=(5, 5), pady=(5, 5))
        self.scrollable_frame2.grid_columnconfigure(0, weight=1)
        

        for i in range(9):
            PLabel = customtkinter.CTkLabel(master=self.scrollable_frame2, text=f"{self.Information_List[i]}",text_color = "white", font=("System", 20, "bold"))
            PLabel.grid(row=i, column=0, padx=10, pady=(10, 10), sticky='w')
            self.Patient_Labels.append(PLabel)
        
        self.First_Name_Entry = customtkinter.CTkEntry(self.scrollable_frame2, width=70, placeholder_text="First")
        self.First_Name_Entry.grid(row=0, column=1,pady=10, padx=(0, 5),sticky="ew")
        
        self.Last_Name_Entry = customtkinter.CTkEntry(self.scrollable_frame2, width=70, placeholder_text="Last")
        self.Last_Name_Entry.grid(row=0, column=2, pady=10, padx=(0,5),sticky="ew")
        
        self.Dob_day_Entry = customtkinter.CTkEntry(self.scrollable_frame2, width=70, placeholder_text="DD")
        self.Dob_day_Entry.grid(row=1, column=1,pady=10, padx=(0, 5),sticky="ew")
        
        self.Dob_month_Entry = customtkinter.CTkEntry(self.scrollable_frame2, width=70, placeholder_text="MM")
        self.Dob_month_Entry.grid(row=1, column=2, pady=10, padx=(0,5),sticky="ew")
        
        self.Dob_year_Entry = customtkinter.CTkEntry(self.scrollable_frame2, width=70, placeholder_text="YYYY")
        self.Dob_year_Entry.grid(row=1, column=3, pady=10, padx=(0,5),sticky="ew")

        self.Gender_Btn = customtkinter.CTkSegmentedButton(self.scrollable_frame2,values=["Male", "Female"])
        self.Gender_Btn.grid(row=2, column=1, padx=(0, 5), pady=(10, 10), sticky="ew")
        
        self.country_var = customtkinter.StringVar(value="Select Country")
        self.country_box = customtkinter.CTkComboBox(master=self.scrollable_frame2, variable=self.country_var, values=self.get_countries(),
                                                          width=220, state="readonly")
        self.country_box.grid(row=3, column=1, pady=10, padx=(0,5), sticky="ew")
        
        self.Disease_Entry = customtkinter.CTkEntry(self.scrollable_frame2, width=70, placeholder_text="Infection, Arthritis...")
        self.Disease_Entry.grid(row=4, column=1, pady=10, padx=(0,5),sticky="ew")
        
        self.Priority_Btn = customtkinter.CTkSegmentedButton(self.scrollable_frame2,values=["High", "Moderate","Low"])
        self.Priority_Btn.grid(row=5, column=1, padx=(0, 5), pady=(10, 10), sticky="ew")
        
        self.Room_Number = customtkinter.CTkEntry(self.scrollable_frame2, width=70, placeholder_text="Unit/Room")
        self.Room_Number.grid(row=6, column=1,pady=10, padx=(0, 5),sticky="ew")
        
        self.Medicine = customtkinter.CTkEntry(self.scrollable_frame2, width=70, placeholder_text="Paracetamol, Aspirin...")
        self.Medicine.grid(row=7, column=1, padx=(0, 5), pady=(10, 10), sticky="ew")
        
        self.Medical_Description_TBOX = customtkinter.CTkTextbox(self.scrollable_frame2, width=240, height=150)
        self.Medical_Description_TBOX.grid(row=8, column=1, padx=(0, 5), pady=(10, 10))
        
        self.Load_Image_Btn = customtkinter.CTkButton(self.scrollable_frame2, text="Register",width=200, font=("System", 30, "bold"), fg_color="#628680", command=lambda:self.Store_Patient())
        self.Load_Image_Btn.grid(row=9, column=1,pady=10,padx=(40,0))

    def Edit_Patient(self, idx):

        edit_window = customtkinter.CTkToplevel(Main, width=200)

        patient_data = self.Patients_Data_Card[idx]

        name_entry = customtkinter.CTkEntry(edit_window, width=200, placeholder_text="Name")
        name_entry.grid(row=0, column=0, padx=50, pady=10)
        name_entry.insert(0, patient_data["name"])
        
        age_entry = customtkinter.CTkEntry(edit_window, width=100, placeholder_text="Age")
        age_entry.grid(row=1, column=0, padx=50, pady=10)
        age_entry.insert(0, patient_data["age"])
        
        room_entry = customtkinter.CTkEntry(edit_window, width=100, placeholder_text="Room Number")
        room_entry.grid(row=2, column=0, padx=50, pady=10)
        room_entry.insert(0, patient_data["room_number"])

        disease_entry = customtkinter.CTkEntry(edit_window, width=100, placeholder_text="Disease")
        disease_entry.grid(row=3, column=0, padx=50, pady=10)
        disease_entry.insert(0, patient_data["disease"])

        apply_button = customtkinter.CTkButton(edit_window, text="Apply", width=200,command=lambda: self.apply_edit(idx, name_entry.get(), age_entry.get(), room_entry.get(), disease_entry.get(), edit_window))
        apply_button.grid(row=4, column=0, padx=50, pady=10)
        
        #EDIT ON DB

    def apply_edit(self, idx, new_name, new_age, new_room, new_disease, edit_window):
        self.Patients_Data_Card[idx]["name"] = new_name
        self.Patients_Data_Card[idx]["age"] = int(new_age)
        self.Patients_Data_Card[idx]["room_number"] = new_room
        self.Patients_Data_Card[idx]["disease"] = new_disease

        self.Patient_Frames_List.clear()
        self.Apply_Patient_Profiles()

        edit_window.destroy()

    def Delete_Patient(self, idx,name):
        if messagebox.askyesno("Delete Patient", "Are you sure you want to delete this patient?"):
            self.Patient_Frames_List[idx].destroy()
            del self.Patients_Data_Card[idx]
            del self.Patient_Frames_List[idx]
            try:
                self.Patient_DB.delete_patient_doc_by_field("name", name)
            except:
                print("Error in deleting patient from database.")
            self.Apply_Patient_Profiles()
            #EDIT ON DB
        
    def Apply_Patient_Profiles(self):
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self.tabview.tab("View Patients"), width=845, height=430)
        self.scrollable_frame.grid(row=0, column=0, padx=(5, 0), pady=(5, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        self.current_path = os.path.dirname(os.path.realpath(__file__))

        max_columns = 3

        for idx, patient_data in enumerate(self.Patients_Data_Card):
            row_index = idx // max_columns
            col_index = idx % max_columns

            self.patient_frame = customtkinter.CTkFrame(
                self.scrollable_frame, corner_radius=20, fg_color="#628680", border_width=5, border_color="black",
                width=250, height=300
            )
            self.patient_frame.grid(row=row_index, column=col_index, padx=10, pady=15)
            self.Patient_Frames_List.append(self.patient_frame)

            image_path = os.path.join(self.current_path, f"Database/Patients/{patient_data['image_path']}")
            patient_image = customtkinter.CTkImage(Image.open(image_path), size=(200, 250))
            self.patient_image_label = customtkinter.CTkLabel(self.patient_frame, image=patient_image, text="")
            self.patient_image_label.grid(row=0, column=0, padx=10, pady=(20, 20))

            patient_description = f"Name: {patient_data['name']}\nAge: {patient_data['age']}\nRoom Number: {patient_data['room_number']}\nDisease/Disability: {patient_data['disease']}"
            self.patient_description_label = customtkinter.CTkLabel(
                self.patient_frame, text=patient_description, text_color="white", font=("System", 20, "bold")
            )
            self.patient_description_label.grid(row=1, column=0, padx=10, pady=(10, 10))

            edit_button = customtkinter.CTkButton(self.patient_frame, text="Edit",fg_color="#FF9A00",hover_color="#FF7400", width=70,command=lambda idx=idx: self.Edit_Patient(idx))
            edit_button.grid(row=3, column=0, padx=(30,10), pady=(5,20), sticky="w")

            delete_button = customtkinter.CTkButton(self.patient_frame, text="Delete", width=70, fg_color="red",hover_color="#C61F1F",command=lambda idx=idx: self.Delete_Patient(idx,patient_data['name']))
            delete_button.grid(row=3, column=0, padx=(10,30), pady=(5,20), sticky="e")
        
        self.progressbar = customtkinter.CTkProgressBar(self.tabview.tab("View Patients"),width=800)
        self.progressbar.place(x=Main.winfo_screenwidth()/2 - 525,y=Main.winfo_screenheight()/2 - 90, anchor="center")

        self.progressbar.configure(mode="indeterminnate")
        self.progressbar.start()
        
        # self.Retreive_Stats()
        self.Load_Stats = True
        
    def Retreive_Stats(self):
        
        cap = cv2.VideoCapture(1)

        while cap.isOpened():
            if(self.start_model and self.Load_Stats):
                # time.sleep(1)
                Ret, Frame = cap.read()
                if not Ret:
                    break
                self.Get_Soft_Stat.Classify(Frame)
                self.Sleep_Stat = self.Get_Soft_Stat.Flag_Sleeping
                # self.Sleep_Stat = "NO"
                self.Eating_Stat = self.Get_Soft_Stat.Flag_Eating
                
                self.X_Gaze = self.Get_Soft_Stat.Eye_X
                self.Y_Gaze = self.Get_Soft_Stat.Eye_Y
                    
                if self.X_Gaze != None and self.Y_Gaze != None:
                    self.X_Gaze = self.Get_Soft_Stat.Eye_X * 1920
                    self.Y_Gaze = self.Get_Soft_Stat.Eye_Y * 1080
                
                self.Expression = self.Get_Soft_Stat.Expression_Status
                print("Facial Expression: ",self.Expression)
                
                Soft_Frame = self.Get_Soft_Stat.Sleep.Frame
                
                #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                
                self.Fall_Stat =  self.Get_Fall_Stat.detect(Frame)
                print("Fall Detection: ",self.Fall_Stat)

                #---------------------------------------------------------------------------------------------------------------------------------------------------------------------
                    
                self.Gesture_Stat = self.Get_Gest_Stat.process_frame(Frame)
                print("Gesture Stat: ", self.Gesture_Stat)

                

                
                cv2.putText(Frame, f"Status: {self.Sleep_Stat,self.Eating_Stat,self.Fall_Stat,self.Gesture_Stat,self.Expression}", (20, 30), cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 0, 0), 2)
                if self.Get_Soft_Stat.Sleep.Start_Time:
                    # cv2.putText(Frame, f"Sleep Timer: {self.Get_Soft_Stat.Sleep.sleep_timer}", (20, 50), cv2.FONT_HERSHEY_PLAIN, 1.2, (255, 0, 0), 2)
                    pass
                cv2.imshow('Patient Monitor', Frame)
                
                
                if (cv2.waitKey(1) & 0xFF == 27 or cv2.getWindowProperty("Patient Monitor", cv2.WND_PROP_VISIBLE) < 1):
                    break
                
                
                try:
                    self.patient1_stat = customtkinter.CTkLabel(self.Patient_Frames_List[0],text = f"Status: {self.Sleep_Stat,self.Eating_Stat}\nRequest: {self.Gesture_Stat}\nEmergency: {self.Fall_Stat}\n Mood: {self.Expression}",text_color="white",font=("System", 10, "bold"))
                    self.patient1_stat.grid(row=2, column=0, padx=10, pady=(20, 20))
                except ValueError as e:
                    print(e)
                    # self.patient1_stat = customtkinter.CTkLabel(self.Patient_Frames_List[0],text = f"Status: {self.Sleep_Stat,self.Eating_Stat}\nRequest: {self.Gesture_Stat}\nEmergency: {self.Fall_Stat}\n Mood: {self.Expression}",text_color="white",font=("System", 10, "bold"))
                    # self.patient1_stat.grid(row=2, column=0, padx=10, pady=(20, 20))
                
                # self.patient2_stat = customtkinter.CTkLabel(self.PPFrame2,text = f"Status: PATIENT NOT PRESENT", fg_color="#B80E0E",text_color="black",font=("System", 20, "bold"))
                # self.patient2_stat.grid(row=2, column=0, padx=20, pady=(20, 20))
                
                # self.patient3_stat= customtkinter.CTkLabel(self.PPFrame3,text = f"Status: PATIENT NOT PRESENT", fg_color="#B80E0E",text_color="black",font=("System", 20, "bold"))
                # self.patient3_stat.grid(row=2, column=0, padx=20, pady=(20, 20))
        
        
        cap.release()
        cv2.destroyAllWindows()
                    

    def set_name(self):
        self.logo_label.configure(text=self.Auth_Name)
        
    def Check_Credentials1(self, Ltype):
        
        self.WarningLabel = customtkinter.CTkLabel(Main, text="Missing Fields...", font=customtkinter.CTkFont(size=20, weight="bold"), fg_color="red")
        self.WarningLabel2 = customtkinter.CTkLabel(Main, text="Wrong Credentials", font=customtkinter.CTkFont(size=20, weight="bold"), fg_color="red")

        if Ltype == "text":
            if self.username_entry.get() == "":
                print("NOT ACCEPTED")
                self.username_entry.configure(bg_color="red")
                self.WarningLabel.place(x=Main.winfo_screenwidth()/2 - 510, y=Main.winfo_screenheight()/2 + 25, anchor="center")
         
            if self.password_entry.get() == "":
                print("NOT ACCEPTED")
                self.password_entry.configure(bg_color="red")
                self.WarningLabel.place(x=Main.winfo_screenwidth()/2 - 510, y=Main.winfo_screenheight()/2 + 25, anchor="center")
           
            if self.username_entry.get() != "" and self.password_entry.get() != "":
                username = self.username_entry.get()
                password = self.password_entry.get()
                for user in self.Nurses:
                    if user["id"] == username and user["password"] == password:
                        self.Auth_Name = user["name"]
                        print("Login User:", self.Auth_Name)
                        self.start_model = True
                        self.Get_Dashboard()
                        break
            else:
                self.WarningLabel2.place(x=Main.winfo_screenwidth()/2 - 510, y=Main.winfo_screenheight()/2 + 25, anchor="center")
        
        elif Ltype == "face":
            Auth = self.Face_System.start_authentication()
            if Auth:
                Nurse_ID, Nurse_Name = Auth
                self.Auth_Name = Nurse_Name
                self.start_model = True
                self.Get_Dashboard() 
            else:
                self.WarningLabel2.place(x=Main.winfo_screenwidth()/2 - 510, y=Main.winfo_screenheight()/2 + 25, anchor="center")
           
    def GoBack_Home(self):
        self.DestroyAll()
        Main.geometry("700x580".format(self.ScreenWidth, self.ScreenHeight))
        self.Main_Screen()
        
    def Login_Page(self):
        self.DestroyAll()
        
        self.width = 900
        self.height = 600
        Main.geometry(f"{self.width}x{self.height}")
        Main.resizable(False, False)
        self.current_path = os.path.dirname(os.path.realpath(__file__))
        self.bg_image = customtkinter.CTkImage(Image.open(self.current_path + "/Assets/thumb-1920-638841.png"),size=(self.width, self.height))
        self.bg_image_label = customtkinter.CTkLabel(Main, image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0)

        self.login_frame = customtkinter.CTkFrame(Main, corner_radius=0)
        self.login_frame.grid(row=0, column=0, sticky="ns")
        self.login_label = customtkinter.CTkLabel(self.login_frame, text="Patient-See\nLogin",
                                                  font=customtkinter.CTkFont(size=20, weight="bold"))
        
        self.current_path = os.path.dirname(os.path.realpath(__file__))
        self.login_image = customtkinter.CTkImage(Image.open(self.current_path + "\Assets\medical-team.png"),size=(200, 200))
        self.login_img_Label = customtkinter.CTkLabel(self.login_frame, image=self.login_image,text = "")
        
        
        self.login_label.grid(row=0, column=0, padx=30, pady=(40, 20))
        self.username_entry = customtkinter.CTkEntry(self.login_frame, width=200, placeholder_text="username")
        self.login_img_Label.grid(row=1, column=0, padx=30, pady=(15, 15))
        self.username_entry.grid(row=2, column=0, padx=30, pady=(15, 15))
        self.password_entry = customtkinter.CTkEntry(self.login_frame, width=200, show="*", placeholder_text="password")
        self.password_entry.grid(row=3, column=0, padx=30, pady=(0, 15))
        self.login_button = customtkinter.CTkButton(self.login_frame, text="Login", command=lambda:self.Check_Credentials1("text"), width=200)
        self.login_button.grid(row=4, column=0, padx=30, pady=(15, 15))
        
        self.Face_button = customtkinter.CTkButton(self.login_frame, text="Use Face", command=lambda:self.Check_Credentials1("face"), width=200)
        self.Face_button.grid(row=5, column=0, padx=30, pady=(10, 10))
        
        self.Back_Btn = customtkinter.CTkButton(Main, text="<- Back",width=80, height=32, font=("System", 20, "bold"), fg_color="DarkRed", command=lambda:self.GoBack_Home())
        self.Back_Btn.place(x=Main.winfo_screenwidth()/2 - 880,y=Main.winfo_screenheight()/2 - 490, anchor="center")


    def Main_Screen(self):
        self.DestroyAll()

        Main.title("Patient-See")
        Main.attributes("-topmost", True)

        self.ScreenWidth = Main.winfo_screenwidth()
        self.ScreenHeight = Main.winfo_screenheight()
        Main.geometry("700x580".format(self.ScreenWidth, self.ScreenHeight))

        self.WelcomeLabel = customtkinter.CTkLabel(Main, text="Patient-See", font=("System", 40, "bold"))
        self.ContinueButton = customtkinter.CTkButton(Main, text="Continue", command=lambda: self.Login_Page(),  width=500, height=125, font=("System", 40, "bold"), fg_color="darkgreen")
        self.QuitButton = customtkinter.CTkButton(Main, text="Quit", command=quit, width=500, height=125, font=("System", 40, "bold"), fg_color="darkgreen")
        self.WelcomeLabel.place(x=self.ScreenWidth/2-610, y=self.ScreenHeight/2 - 450, anchor="center")
        self.ContinueButton.place(x=self.ScreenWidth/2 - 610, y=self.ScreenHeight/2 - 250, anchor="center")
        self.QuitButton.place(x=self.ScreenWidth/2 - 610, y=self.ScreenHeight/2 - 100, anchor="center")

gui = MainGUI()
def camera_thread():
    gui.Retreive_Stats()

gui_thread = threading.Thread(target=gui.Main_Screen)
cam_thread = threading.Thread(target=camera_thread)

gui_thread.start()
cam_thread.start()


Main.mainloop()

