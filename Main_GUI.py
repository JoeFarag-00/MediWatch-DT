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
from bson.objectid import ObjectId
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
        self.IsRefreshed = False
        self.Patient_Frames_List = []
        self.Nurse_Frames_List = []
        
        self.PushRow = None
        self.PushCol = None
        self.EmptyDB = False
        
         
        self.Patients_Data_Card_DB = []
        self.Patients_IDs = []
        
        self.Nurse_Data_Card = [
            {"name": "Abdo Moota", "age": 47, "qualifications": "Doctor", "department_id": "D122","contact_number": "01024985562","gender":"Male","floor_number":3 ,"image_path": "Abdo.png"},
            {"name": "Hamada Hamdoon ", "age": 26,"qualifications": "EMT", "department_id": "A132", "contact_number": "01553309309","gender":"Male","floor_number":3 ,"image_path": "Hamada.png"},
            {"name": "Sabrina Sabarny", "age": 30, "qualifications": "Nurse", "department_id": "D126", "contact_number": "0103668966","gender":"Female","floor_number":2 ,"image_path": "Sabrina.png"},
            {"name": "Samantha Rohantha", "age": 27, "qualifications": "Nurse", "department_id": "G1252", "contact_number": "0102984552","gender":"Female","floor_number":1 ,"image_path": "Samantha.png"},
        ]
        
        self.medlist = []
        self.Patient_Labels = []
        self.Information_List = ["Patient Name: ", "DOB: ", "Gender: ", "Nationality: ", "Complication: ", "Priority Care: ", "Room Number: ", "Medicines: " ,"Medical Description: "]
        self.Long_Infolist = ["Patient Name: ", "DOB: ","Age: ", "Gender: ", "Nationality: ", "Room Number: " ,"Complication: ", "Priority Care: ", "Medicines: " ,"Medical Description: "]
        self.Nurses_Auth = [
        {"id": "211777", "password": "1234","name": "Youssef"},
        {"id": "212257", "password": "1234","name": "Mina"},
        ]
        
        self.Get_Gest_Stat = HandGestureProcessor()
        self.Get_Soft_Stat = Soft_Behavior_Detector()
        self.Get_Fall_Stat = FallDetector()
        self.Face_System = FaceIdentificationSystem(known_nurses=self.Nurses_Auth)
        self.Patient_DB = Patient()
        self.Nurse_DB = Nurse()
        # self.MediTUIO = Medicine_TUIO()

        self.Patients_Data_Card_DB = self.Patient_DB.read_all_patients()
        print(self.Patients_Data_Card_DB)

        i=0
        for patient in self.Patients_Data_Card_DB:
            self.Patients_IDs.append(patient["_id"])
            print(f"Patient {i}: ",  patient["_id"],"\n")
            i+=1
        
    
        if len(self.Patients_Data_Card_DB) == 0:
            self.EmptyDB = True


        self.image_path = None

    @staticmethod
    def DestroyAll():
        widgets = Main.winfo_children()
        for widget in widgets:
            widget.destroy()

    def Exit(self):
        os._exit(0)
        
    def Refresh_New(self):
        self.Patients_Data_Card_DB = self.Patient_DB.read_all_patients()
        self.DestroyAll()
        self.Get_Dashboard()
        self.IsRefreshed = True
        self.Retreive_Stats()
        


    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def Get_Dashboard(self):
        self.DestroyAll()
        self.Patients_Data_Card_DB = self.Patient_DB.read_all_patients()
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
        
        self.Refresh_Button = customtkinter.CTkButton(self.sidebar_frame, text="Refresh", command=self.Refresh_New)
        self.Refresh_Button.grid(row=2, column=0, padx=20, pady=10)
        
        self.Heat_Map_Btn = customtkinter.CTkButton(self.sidebar_frame, text="Generate Heat", command=self.Generate_Heat_Map)
        self.Heat_Map_Btn.grid(row=4, column=0, padx=20, pady=10)
        
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
    
    def Generate_Heat_Map(self):
        heat_window = customtkinter.CTkToplevel(Main, width=200)
        self.Get_Soft_Stat.Gaze_Tracking.Generate_Heatmap()
        self.Patient_img = customtkinter.CTkImage(Image.open("Behavior_Models/Soft Behaviors/Heatmap.png"),size=(500, 500))
        self.Patientimg_Label = customtkinter.CTkLabel(heat_window, image=self.Patient_img,text = "")
        self.Patientimg_Label.grid(row=0, column=0, padx=20, pady=(20, 20))
    

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

    def Get_Age_DOB(self,Date):
        try:
            # Date = self.Dob_day_Entry.get() + "/" + self.Dob_month_Entry.get() + "/" + self.Dob_year_Entry.get()
            dob_date = datetime.strptime(Date, "%d/%m/%Y")
            current_date = datetime.now()
            age = current_date.year - dob_date.year - ((current_date.month, current_date.day) < (dob_date.month, dob_date.day))
            return age
        except ValueError as e:
            print("Error in Calculating Age: ", e)
            return 0
        
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
    
    def check_for_duplicate(self, entry):
        entry_id = entry.get('_id')
        for patient in self.Patients_Data_Card_DB:
            if all(patient[attr] == entry[attr] for attr in patient if attr != '_id'):
                return True 

        return False

    def check_for_DupRoom(self, entry):
        existing_room_numbers = set(patient["room_no"] for patient in self.Patients_Data_Card_DB)
        if entry["room_number"] in existing_room_numbers:
            return True
        else:
            return False
    
        
    def Store_Patient(self):
        self.Patients_Data_Card_DB = self.Patient_DB.read_all_patients()
        self.WarningLabel = customtkinter.CTkLabel(Main, text="Missing Fields...", font=customtkinter.CTkFont(size=20, weight="bold"),text_color="red" )
        if self.image_path and self.First_Name_Entry.get() and self.Last_Name_Entry.get() and self.Dob_day_Entry.get() and self.Dob_month_Entry.get() and self.Dob_year_Entry.get() and self.Gender_Btn.get() and self.country_box.get() != "Select Country" and self.Disease_Entry.get() and self.Priority_Btn.get() and self.Medicine.get() and self.Medical_Description_TBOX.get('0.0','end'):
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
                        dob = self.Dob_day_Entry.get() + '/' + self.Dob_month_Entry.get() + '/' + self.Dob_year_Entry.get()
                        Age = self.Get_Age_DOB(dob)
                        gender = self.Gender_Btn.get()
                        nationality = self.country_box.get()
                        room_num = self.Room_Number.get()
                        disease = self.Disease_Entry.get()
                        medlist = [obj.strip() for obj in self.Medicine.get().split(',')]
                        Priority_Care = self.Priority_Btn.get()
                        Medical_Desc = self.Medical_Description_TBOX.get('0.0','end')
                        # image_binary = self.Patient_DB.write_image(self.image_path)
                        path = file_name
                        image_binary = "None"
                        
                        new_patient = {"_id":"NONE","name": Name,"DOB":dob , "age":Age ,"gender": gender,"nationality":nationality,"room_number": room_num, "disease": disease, "prioritycare":Priority_Care, "medicines": medlist,"Medical_Desc": Medical_Desc,"image_path": file_name,"image_data":image_binary}
                        AskDup = self.check_for_duplicate(new_patient)
                        AskDupRoom = self.check_for_DupRoom(new_patient)
                    
                        if not AskDup:
                            if not AskDupRoom:
                                messagebox.showinfo("Added Patient details", f"Patient '{Name}' Added, Please Refresh")
                                Patient_ID = self.Patient_DB.create_patient_doc(Name, dob, Age, gender, nationality, room_num, disease, medlist, Priority_Care, Medical_Desc, path, image_binary)
                                self.Patients_IDs.append(Patient_ID)
                                
                                print(f"Patient Name:{self.First_Name_Entry.get()+' '+self.Last_Name_Entry.get()}\n",
                                f"DOB: {self.Dob_day_Entry.get() + '/' + self.Dob_month_Entry.get() + '/' + self.Dob_year_Entry.get()}\n", 
                                f"Age: {self.Get_Age_DOB(dob)}\n",
                                f"Gender: {self.Gender_Btn.get()}\n", 
                                f"Nationality: {self.country_box.get()}\n", 
                                f"Complication: {self.Disease_Entry.get()}\n",
                                f"Priority Care: {self.Priority_Btn.get()}\n",
                                f"Room: {self.Room_Number.get()}"
                                f"Medical Description: {self.Medical_Description_TBOX.get('0.0','end')}\n")
                            
                                # new_patient = {"_id":Patient_ID,"name": Name,"DOB":dob , "age":Age ,"gender": gender,"nationality":nationality,"room_number": room_num, "disease": disease, "prioritycare":Priority_Care, "medicines": medlist,"Medical_Desc": Medical_Desc,"image_path": file_name,"image_data":image_binary}
                                # self.Patients_Data_Card_DB.append(new_patient)
                                print("DATABASE:\n",self.Patients_Data_Card_DB)
                                self.First_Name_Entry.delete(0,100)
                                self.Last_Name_Entry.delete(0,100)
                                self.Dob_day_Entry.delete(0,100)
                                self.Dob_month_Entry.delete(0,100) 
                                self.Dob_year_Entry.delete(0,100) 
                                self.Gender_Btn.set("")
                                self.country_box.set("Select Country")
                                self.Disease_Entry.delete(0,100)
                                self.Priority_Btn.set("")
                                self.Room_Number.delete(0,100)
                                self.Medicine.delete(0,100) 
                                self.Medical_Description_TBOX.delete("0.0","end")
                                self.Patientimg_Label.destroy()
                                self.image_path = None
                            
                            
                            else:
                                messagebox.showerror("Error", f"A Patient with this room number already exists.")

                        else:
                            messagebox.showerror("Error", f"A Patient with this information already exists.")
                 

                        self.Apply_Patient_Profiles()
                        # self.Retreive_Stats()
                        
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

    def Change_Patient_Image(self, idx,LoadImg_Frame ,patient_img, patientLbl):
        image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")])
        
        if image_path:
            patient_img = customtkinter.CTkImage(Image.open(image_path),size=(210, 250))
            patientLbl = customtkinter.CTkLabel(LoadImg_Frame, image=patient_img,text = "")
            patientLbl.grid(row=0, column=0, padx=20, pady=(20, 20))
            
            destination_folder = "Database/Patients" 
            
            file_name = os.path.basename(image_path)
            destination_path = os.path.join(destination_folder, file_name)
            try:
                copyfile(image_path, destination_path)
                print(f"Image '{file_name}' successfully copied to '{destination_folder}'")
                self.Edit_Patient_Data["image_path"] = file_name
                print("new file: ",self.Edit_Patient_Data["image_path"])

            except Exception as e:
                print(f"Error copying image: {e}")
                
                
    def Edit_Patient(self, idx):

        edit_window = customtkinter.CTkToplevel(Main, width=400, height=400)
        # self.Patients_Data_Card_DB = self.Patient_DB.read_all_patients()
        # print(self.Patients_Data_Card_DB[idx]["image_path"])
        self.Edit_Patient_Data = self.Patients_Data_Card_DB[idx]
        print(self.Edit_Patient_Data["image_path"])
        
        Patient_Picture_Frame = customtkinter.CTkFrame(edit_window, width=550,height=430)
        Patient_Picture_Frame.grid(row=0, column=0, padx=(30, 20), pady=(10, 10))
        
        LoadImg_Frame = customtkinter.CTkFrame(Patient_Picture_Frame, corner_radius=20, fg_color="#628680",border_width=5, border_color="black",width=250,height=300)
        LoadImg_Frame.grid(row=0, column=0,pady=(30,20))
        
        # print(patient_data[idx]['image_path'])
        Patient_img = customtkinter.CTkImage(Image.open(f"Database/Patients/{self.Edit_Patient_Data['image_path']}"),size=(210, 250))
        
        Patientimg_Label = customtkinter.CTkLabel(LoadImg_Frame, image=Patient_img,text = "")
        Patientimg_Label.grid(row=0, column=0, padx=20, pady=(20, 20))
        
        rm_Image_Btn = customtkinter.CTkButton(Patient_Picture_Frame, text="Change Picture",width=200, font=("System", 30, "bold"), fg_color="#FF8600", hover_color="#FF3200", command=lambda:self.Change_Patient_Image(idx, LoadImg_Frame,Patient_img,Patientimg_Label))
        rm_Image_Btn.grid(row=1, column=0,pady=20)
        
        
        scrollable_frame2 = customtkinter.CTkScrollableFrame(edit_window, width=550,height=430)
        scrollable_frame2.grid(row=0, column=1, padx=(5, 5), pady=(5, 5))
        scrollable_frame2.grid_columnconfigure(0, weight=1)
        
        Patient_Labels = []
        for i in range(9):
            PLabel = customtkinter.CTkLabel(master=scrollable_frame2, text=f"{self.Information_List[i]}",text_color = "white", font=("System", 20, "bold"))
            PLabel.grid(row=i, column=0, padx=10, pady=(10, 10), sticky='w')
            Patient_Labels.append(PLabel)
        
        # First_Name_Entry = customtkinter.CTkEntry(self.scrollable_frame2, width=70, placeholder_text="First")
        # First_Name_Entry.grid(row=0, column=1,pady=10, padx=(0, 5),sticky="ew")
        
        # Last_Name_Entry = customtkinter.CTkEntry(self.scrollable_frame2, width=70, placeholder_text="Last")
        # Last_Name_Entry.grid(row=0, column=2, pady=10, padx=(0,5),sticky="ew")

        # Dob_day_Entry = customtkinter.CTkEntry(self.scrollable_frame2, width=70, placeholder_text="DD")
        # Dob_day_Entry.grid(row=1, column=1,pady=10, padx=(0, 5),sticky="ew")
        
        # Dob_month_Entry = customtkinter.CTkEntry(self.scrollable_frame2, width=70, placeholder_text="MM")
        # Dob_month_Entry.grid(row=1, column=2, pady=10, padx=(0,5),sticky="ew")
        
        # Dob_year_Entry = customtkinter.CTkEntry(self.scrollable_frame2, width=70, placeholder_text="YYYY")
        # Dob_year_Entry.grid(row=1, column=3, pady=10, padx=(0,5),sticky="ew")

        # Gender_Btn = customtkinter.CTkSegmentedButton(self.scrollable_frame2,values=["Male", "Female"])
        # Gender_Btn.grid(row=2, column=1, padx=(0, 5), pady=(10, 10), sticky="ew")
        
        # country_var = customtkinter.StringVar(value="Select Country")
        # country_box = customtkinter.CTkComboBox(master=self.scrollable_frame2, variable=self.country_var, values=self.get_countries(),
        #                                                   width=220, state="readonly")
        # country_box.grid(row=3, column=1, pady=10, padx=(0,5), sticky="ew")
        
        # Disease_Entry = customtkinter.CTkEntry(self.scrollable_frame2, width=70, placeholder_text="Infection, Arthritis...")
        # Disease_Entry.grid(row=4, column=1, pady=10, padx=(0,5),sticky="ew")
        
        # Priority_Btn = customtkinter.CTkSegmentedButton(self.scrollable_frame2,values=["High", "Moderate","Low"])
        # Priority_Btn.grid(row=5, column=1, padx=(0, 5), pady=(10, 10), sticky="ew")
        
        # Room_Number = customtkinter.CTkEntry(self.scrollable_frame2, width=70, placeholder_text="Unit/Room")
        # Room_Number.grid(row=6, column=1,pady=10, padx=(0, 5),sticky="ew")
        
        # Medicine = customtkinter.CTkEntry(self.scrollable_frame2, width=70, placeholder_text="Paracetamol, Aspirin...")
        # Medicine.grid(row=7, column=1, padx=(0, 5), pady=(10, 10), sticky="ew")
        
        # Medical_Description_TBOX = customtkinter.CTkTextbox(self.scrollable_frame2, width=240, height=150)
        # Medical_Description_TBOX.grid(row=8, column=1, padx=(0, 5), pady=(10, 10))
        
        # Load_Image_Btn = customtkinter.CTkButton(self.scrollable_frame2, text="Register",width=200, font=("System", 30, "bold"), fg_color="#628680", command=lambda:self.Store_Patient())
        # Load_Image_Btn.grid(row=9, column=1,pady=10,padx=(40,0))

    def Apply_Edit(self, idx, name, dob, gender, nationality, room_no, disease, medicines,edit_window):
        self.Patients_Data_Card_DB[idx]["name"] = name
        self.Patients_Data_Card_DB[idx]["dob"] = dob
        self.Patients_Data_Card_DB[idx]["age"] = self.Get_Age_DOB(dob)
        self.Patients_Data_Card_DB[idx]["gender"] = gender
        self.Patients_Data_Card_DB[idx]["room_no"] = room_no
        self.Patients_Data_Card_DB[idx]["disease"] = disease
        self.Patients_Data_Card_DB[idx]["medicines"] = disease


        self.Patient_Frames_List.clear()
        self.Apply_Patient_Profiles()

        edit_window.destroy()

    def Delete_Patient(self, idx,name):
        if messagebox.askyesno("Remove Patient Card", "Are you sure you want to remove this patient?"):
            self.Patient_Frames_List[idx].destroy()
            del self.Patients_Data_Card_DB[idx]
            del self.Patient_Frames_List[idx]
            try:
                self.Patient_DB.delete_patient_doc_by_field("name", name)
            except:
                print("Error in deleting patient from database.")
            self.Apply_Patient_Profiles()
            
        # if messagebox.askyesno("Remove Patient Card", "Are you sure you want to remove this patient?"):
        #     self.Patient_Frames_List[idx].destroy()
        #     del self.Patients_Data_Card_DB[idx]
        #     del self.Patient_Frames_List[idx]
        #     try:
        #         self.Patient_DB.delete_patient_doc_by_field("name", name)
        #     except:
        #         print("Error in deleting patient from database.")
        #     self.Apply_Patient_Profiles()
            
    def Show_Patient_Info(self, idx):
        Info_Window = customtkinter.CTkToplevel(Main, width=800, height=500)
        patient_data = self.Patients_Data_Card_DB[idx]

        patient_frame = customtkinter.CTkFrame(Info_Window, corner_radius=20, fg_color="#628680", border_width=5, border_color="black",width=250, height=300)
        patient_frame.grid(row=0, column=0, padx=10, pady=15)

        image_path = os.path.join(self.current_path, f"Database/Patients/{patient_data['image_path']}")
        patient_image = customtkinter.CTkImage(Image.open(image_path), size=(200, 250))
        
        self.patient_image_label = customtkinter.CTkLabel(patient_frame, image=patient_image, text="")
        self.patient_image_label.grid(row=0, column=0, padx=10, pady=(20, 20))
        
        for i in range(10):
            PLabel = customtkinter.CTkLabel(master=Info_Window, text=f"{self.Long_Infolist[i]}",text_color = "white", font=("System", 20, "bold"))
            PLabel.grid(row=i+1, column=0, padx=10, pady=(10, 10), sticky='w')
            
            
        NameLabel = customtkinter.CTkLabel(master=Info_Window, text=f"{self.Patients_Data_Card_DB[idx]['name']}",text_color = "white", font=("System", 20, "bold"))
        NameLabel.grid(row=1, column=1, padx=10, pady=(10, 10), sticky='w')
        
        dob_label = customtkinter.CTkLabel(master=Info_Window, text=f"{self.Patients_Data_Card_DB[idx]['DOB']}",text_color = "white", font=("System", 20, "bold"))
        dob_label.grid(row=2, column=1, padx=10, pady=(10, 10), sticky='w')
        
        age_label = customtkinter.CTkLabel(master=Info_Window, text=f"{self.Patients_Data_Card_DB[idx]['age']}",text_color = "white", font=("System", 20, "bold"))
        age_label.grid(row=3, column=1, padx=10, pady=(10, 10), sticky='w')
        
        gender_label = customtkinter.CTkLabel(master=Info_Window, text=f"{self.Patients_Data_Card_DB[idx]['gender']}",text_color = "white", font=("System", 20, "bold"))
        gender_label.grid(row=4, column=1, padx=10, pady=(10, 10), sticky='w')
        
        nationality_label = customtkinter.CTkLabel(master=Info_Window, text=f"{self.Patients_Data_Card_DB[idx]['nationality']}",text_color = "white", font=("System", 20, "bold"))
        nationality_label.grid(row=5, column=1, padx=10, pady=(10, 10), sticky='w')
        
        room_label = customtkinter.CTkLabel(master=Info_Window, text=f"{self.Patients_Data_Card_DB[idx]['room_no']}",text_color = "white", font=("System", 20, "bold"))
        room_label.grid(row=6, column=1, padx=10, pady=(10, 10), sticky='w')
        
        disease_label = customtkinter.CTkLabel(master=Info_Window, text=f"{self.Patients_Data_Card_DB[idx]['disease']}",text_color = "white", font=("System", 20, "bold"))
        disease_label.grid(row=7, column=1, padx=10, pady=(10, 10), sticky='w')
        
        priority_label = customtkinter.CTkLabel(master=Info_Window, text=f"{self.Patients_Data_Card_DB[idx]['Priority_Care']}",text_color = "white", font=("System", 20, "bold"))
        priority_label.grid(row=8, column=1, padx=10, pady=(10, 10), sticky='w')
        
        medicine_label = customtkinter.CTkLabel(master=Info_Window, text=f"{self.Patients_Data_Card_DB[idx]['medicines']}",text_color = "white", font=("System", 20, "bold"))
        medicine_label.grid(row=9, column=1, padx=10, pady=(10, 10), sticky='w')

        medical_desLabel = customtkinter.CTkLabel(master=Info_Window, text=f"{self.Patients_Data_Card_DB[idx]['Medical_Desc']}",text_color = "white", font=("System", 20, "bold"))
        medical_desLabel.grid(row=10, column=1, padx=10, pady=(10, 10), sticky='w')
        

        # self.Patients_Data_Card_DB[idx]["age"] 
        # self.Patients_Data_Card_DB[idx]["room_number"]
        # self.Patients_Data_Card_DB[idx]["disease"]
        
    def Apply_Patient_Profiles(self):
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self.tabview.tab("View Patients"), width=845, height=430)
        self.scrollable_frame.grid(row=0, column=0, padx=(5, 0), pady=(5, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        self.current_path = os.path.dirname(os.path.realpath(__file__))
        
        # self.Patient_DB.read_specific_patient_by_name("")        
        max_columns = 3
        if not self.EmptyDB:
            for idx, patient_data in enumerate(self.Patients_Data_Card_DB):
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
                # self.patient_image_label = customtkinter.CTkLabel(self.patient_frame, image=patient_image, text="")
                # self.patient_image_label.grid(row=0, column=0, padx=10, pady=(20, 20))
                
                self.patient_image_button = customtkinter.CTkButton(self.patient_frame,text="",hover_color="#F3D6D6",fg_color="#628680",image=patient_image, width=100,height=100,command=lambda idx=idx: self.Show_Patient_Info(idx))
                self.patient_image_button.grid(row=0, column=0, padx=10, pady=(10, 10))

                patient_description = f"Name: {patient_data['name']}\nAge: {patient_data['age']}\nRoom Number: {patient_data['room_no']}\nDisease/Disability: {patient_data['disease']}\nPriority Care: {patient_data['Priority_Care']}"
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
        # cap = cv2.VideoCapture(2)

        while cap.isOpened():
            if(self.start_model and self.Load_Stats):
                # time.sleep(1)
                Ret, Frame = cap.read()
                if not Ret or self.IsRefreshed:
                    self.IsRefreshed = False
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
                    cv2.putText(Frame, f"Sleep Timer: {self.Get_Soft_Stat.Sleep.Timer}", (20, 50), cv2.FONT_HERSHEY_PLAIN, 1.2, (255, 0, 0), 2)
                    pass
                cv2.imshow('Patient Monitor', Frame)
                
                
                if (cv2.waitKey(1) & 0xFF == 27 or cv2.getWindowProperty("Patient Monitor", cv2.WND_PROP_VISIBLE) < 1):
                    break
                
                
      
                try:
                    self.patient1_stat = customtkinter.CTkLabel(self.Patient_Frames_List[0], text=f"Status: {self.Sleep_Stat, self.Eating_Stat}\nRequest: {self.Gesture_Stat}\nMood: {self.Expression}\nEmergency: {self.Fall_Stat}", text_color="white", font=("System", 10, "bold"))
                    self.patient1_stat.grid(row=2, column=0, padx=10, pady=(20, 20))

                    if self.Fall_Stat == "Safe":
                        self.patient1_stat = customtkinter.configure(self.Patient_Frames_List[0], text=f"Status: {self.Sleep_Stat, self.Eating_Stat}\nRequest: {self.Gesture_Stat}\nMood: {self.Expression}\nEmergency: {self.Fall_Stat}", text_color="white", font=("System", 10, "bold"))
                        self.patient1_stat.grid(row=2, column=0, padx=10, pady=(20, 20))
                    elif self.Fall_Stat == "Fall":
                        self.patient1_stat = customtkinter.CTkLabel(self.Patient_Frames_List[0], text=f"Status: {self.Sleep_Stat, self.Eating_Stat}\nRequest: {self.Gesture_Stat}\nMood: {self.Expression}\nEmergency: {self.Fall_Stat}", fg_color="red", font=("System", 10, "bold"))
                        self.patient1_stat.grid(row=2, column=0, padx=10, pady=(20, 20))
                except Exception as e:
                    print(f"Error In Stat")

                    
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
                for user in self.Nurses_Auth:
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
        self.login_label = customtkinter.CTkLabel(self.login_frame, text="Medi-Watch\nLogin",
                                                  font=customtkinter.CTkFont(size=20, weight="bold"))
        
        self.current_path = os.path.dirname(os.path.realpath(__file__))
        self.login_image = customtkinter.CTkImage(Image.open(self.current_path + "/Assets/mediwatch.png"),size=(200, 200))
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

        Main.title("Medi-Watch")
        Main.attributes("-topmost", True)

        self.ScreenWidth = Main.winfo_screenwidth()
        self.ScreenHeight = Main.winfo_screenheight()
        Main.geometry("700x580".format(self.ScreenWidth, self.ScreenHeight))

        self.WelcomeLabel = customtkinter.CTkLabel(Main, text="Medi-Watch", font=("System", 40, "bold"))
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
# cam_thread.start()


Main.mainloop()

