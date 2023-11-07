import customtkinter
import os
import threading
from tkinter import Tk
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
import sys
import socket

Main = customtkinter.CTk()

class MainGUI:
    def __init__(self):
        self.Main = Main
        self.start_model = False

    @staticmethod
    def DestroyAll():
        widgets = Main.winfo_children()
        for widget in widgets:
            widget.destroy()

    def Continue(self):
        self.DestroyAll()
        self.Login_Page()

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
        self.name = "Nurse"
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
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Chats", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=1, column=0, padx=20)
        
        self.Profile_Button = customtkinter.CTkButton(self.sidebar_frame, text="Profile")
        self.Profile_Button.grid(row=2, column=0, padx=20, pady=10)
        
        self.Settings_Button = customtkinter.CTkButton(self.sidebar_frame, text="Settings")
        self.Settings_Button.grid(row=4, column=0, padx=20, pady=10)
        
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_options = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_options.grid(row=5, column=0, padx=20, pady=(10, 10))
        self.exit_button = customtkinter.CTkButton(self.sidebar_frame, text="Exit", hover_color="Red", command=self.Exit)
        self.exit_button.grid(row=6, column=0, padx=20, pady=10)
        self.tabview = customtkinter.CTkTabview(master=self.Main, width=250, height=490)
        self.tabview.grid(row=1, column=1, columnspan=2, padx=(20, 10), pady=(10, 0), sticky="nsew")
        self.tabview.add("View Patients")
        self.tabview.set("View Patients")
        self.tabview.add("Register patients")
        self.tabview.add("Active Nurses")
        self.set_name()
        self.Apply_Patient_Profiles()

            
    def Apply_Patient_Profiles(self):
        
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self.tabview.tab("View Patients"), width=845,height=430)
        self.scrollable_frame.grid(row=0, column=0, padx=(5, 0), pady=(5, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        self.current_path = os.path.dirname(os.path.realpath(__file__))
        
        #----------------------------------------
        
        self.PPFrame1 = customtkinter.CTkFrame(self.scrollable_frame, corner_radius=20, fg_color="#2fa572",border_width=5, border_color="black",width=250,height=300)
        self.PPFrame1.grid(row=0, column=0, padx=10,pady=20)

        self.patient1 = customtkinter.CTkImage(Image.open(self.current_path + "\Assets\Patients\me.jpg"),size=(140, 150))
        self.patient1_bg = customtkinter.CTkLabel(self.PPFrame1, image=self.patient1,text = "")
        self.patient1_bg.grid(row=0, column=0, padx=20, pady=(20, 20))
        
        self.patient1_Description = customtkinter.CTkLabel(self.PPFrame1,text = f"Name: Youssef Mohamed\n Age: 20\nRoom Number: G103A\n Disease/Disability: Success", text_color = "white",font=("System", 20, "bold"))
        self.patient1_Description.grid(row=1, column=0, padx=20, pady=(20, 20))

        #-----------------------------
        
        self.PPFrame2 = customtkinter.CTkFrame(self.scrollable_frame, corner_radius=20, fg_color="#2fa572",border_width=5, border_color="black",width=250,height=300)
        self.PPFrame2.grid(row=0, column=1,padx=50,pady=20)

        self.patient2 = customtkinter.CTkImage(Image.open(self.current_path + "\Assets\Patients\mina.jpg"),size=(140, 150))
        self.patient2_bg = customtkinter.CTkLabel(self.PPFrame2, image=self.patient2,text = "")
        self.patient2_bg.grid(row=0, column=0, padx=20, pady=(20, 20))
        
        self.patient2_Description = customtkinter.CTkLabel(self.PPFrame2,text = "Name: Mina Samir\n Age: 21\nRoom Number: G408A\n Disease/Disability: Alzheimer's",text_color = "white",font=("System", 20, "bold"))
        self.patient2_Description.grid(row=1, column=0, padx=20, pady=(20, 20))
        
        #----------------------------------------
        
        self.PPFrame3 = customtkinter.CTkFrame(self.scrollable_frame, corner_radius=20, fg_color="#2fa572",border_width=5, border_color="black",width=250,height=300)
        self.PPFrame3.grid(row=0, column=2,padx=10,pady=20)

        self.patient3 = customtkinter.CTkImage(Image.open(self.current_path + "\Assets\Patients\steven.jpg"),size=(140, 150))
        self.patient3_bg = customtkinter.CTkLabel(self.PPFrame3, image=self.patient3,text = "")
        self.patient3_bg.grid(row=0, column=0, padx=20, pady=(20, 20))
        
        self.patient3_Description = customtkinter.CTkLabel(self.PPFrame3,text = "Name: Steven Hany\n Age: 21\nRoom Number: D101\n Disease/Disability: Anger",text_color = "white",font=("System", 20, "bold"))
        self.patient3_Description.grid(row=1, column=0, padx=20, pady=(20, 20))
        
        #-----------------------------------------
        
        self.PPFrame4 = customtkinter.CTkFrame(self.scrollable_frame, corner_radius=20, fg_color="#2fa572",border_width=5, border_color="black",width=250,height=300)
        self.PPFrame4.grid(row=1, column=0,padx=10, pady=20)

        self.patient4 = customtkinter.CTkImage(Image.open(self.current_path + "\Assets\Patients\pola2.jpg"),size=(140, 150))
        self.patient4_bg = customtkinter.CTkLabel(self.PPFrame4, image=self.patient4,text = "")
        self.patient4_bg.grid(row=0, column=0, padx=20, pady=(20, 20))
        
        self.patient4_Description = customtkinter.CTkLabel(self.PPFrame4,text = "Name: Pola Emanuel\n Age: 21\nRoom Number: E205\n Disease/Disability: None",text_color = "white",font=("System", 20, "bold"))
        self.patient4_Description.grid(row=1, column=0, padx=20, pady=(20, 20))
        
        #-----------------------------------------
        
        self.progressbar = customtkinter.CTkProgressBar(self.tabview.tab("View Patients"),width=800)
        self.progressbar.place(x=Main.winfo_screenwidth()/2 - 525,y=Main.winfo_screenheight()/2 - 90, anchor="center")

        self.progressbar.configure(mode="indeterminnate")
        self.progressbar.start()
        
        # self.Retreive_Stats()
        
    def Retreive_Stats(self):
        
        sys.path.append('Behavior_Models/Soft Behaviors')
        from Soft_Behavior_Detector import Soft_Behavior_Detector
        Get_Soft_Stat = Soft_Behavior_Detector()
        cap = cv2.VideoCapture(1)

        while cap.isOpened():
            if(self.start_model):
                time.sleep(1)
                Ret, Frame = cap.read()
                if not Ret:
                    break
                Get_Soft_Stat.Classify(Frame)
                self.Sleep_Stat = Get_Soft_Stat.Flag_Sleeping
                self.Eating_Stat = Get_Soft_Stat.Flag_Eating
                print(f"Soft Behaviors Stat: {self.Sleep_Stat}, {self.Eating_Stat}")
                Soft_Frame = Get_Soft_Stat.Sleep.Frame
                cv2.putText(Frame, str(self.Eating_Stat), (200, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                cv2.imshow('Soft Behavior', Soft_Frame)

                if (cv2.waitKey(1) & 0xFF == 27 or cv2.getWindowProperty("Soft Behavior", cv2.WND_PROP_VISIBLE) < 1):
                    break
                
                # self.patient1_stat = customtkinter.CTkLabel(self.PPFrame1,text = "Status: ", fg_color="#FF8157",text_color="black",font=("System", 20, "bold"))
                # self.patient1_stat.grid(row=2, column=0, padx=20, pady=(20, 20))
                
                # self.patient2_stat = customtkinter.CTkLabel(self.PPFrame2,text = "Status: ", fg_color="#FF8157",text_color="black",font=("System", 20, "bold"))
                # self.patient2_stat.grid(row=2, column=0, padx=20, pady=(20, 20))
                
                # self.patient3_stat = customtkinter.CTkLabel(self.PPFrame3,text = "Status: ", fg_color="#FF8157",text_color="black",font=("System", 20, "bold"))
                # self.patient3_stat.grid(row=2, column=0, padx=20, pady=(20, 20))
                
                # if(self.Gesture_Stat != "fist-hand"):
                #     self.patient1_stat.configure(self.PPFrame1,text = f"Status: {self.Sleep_Stat,self.Eating_Stat}", fg_color="#FF8157",text_color="black",font=("System", 20, "bold"))
                #     self.patient1_stat.grid(row=2, column=0, padx=20, pady=(20, 20))
                    
                #     self.patient2_stat.configure(self.PPFrame2,text = f"Status: {self.Sleep_Stat,self.Eating_Stat}", fg_color="#FF8157",text_color="black",font=("System", 20, "bold"))
                #     self.patient2_stat.grid(row=2, column=0, padx=20, pady=(20, 20))
                    
                #     self.patient3_stat.configure(self.PPFrame3,text = f"Status: {self.Sleep_Stat,self.Eating_Stat}", fg_color="#FF8157",text_color="black",font=("System", 20, "bold"))
                #     self.patient3_stat.grid(row=2, column=0, padx=20, pady=(20, 20))
                
                #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                sys.path.append('Behavior_Models/Hand Gesture')
                from hand_gesture import HandGestureRecognition
                
                Get_Gest_Stat = HandGestureRecognition()
                
                self.Gesture_tuple = Get_Gest_Stat.hand_gesture(Frame)
                self.Gesture_Stat = str(self.Gesture_tuple[0])
                print("Gesture Stat: ",self.Gesture_Stat)
                
                # if(self.Gesture_Stat == "fist-hand"):
                    
                #     self.patient1_stat.configure(self.PPFrame1,text = f"Status: {self.Gesture_Stat}", fg_color="#FF8157",text_color="black",font=("System", 20, "bold"))
                #     self.patient1_stat.grid(row=2, column=0, padx=20, pady=(20, 20))
                    
                #     self.patient2_stat.configure(self.PPFrame2,text = f"Status: {self.Gesture_Stat}", fg_color="#FF8157",text_color="black",font=("System", 20, "bold"))
                #     self.patient2_stat.grid(row=2, column=0, padx=20, pady=(20, 20))
                    
                #     self.patient3_stat.configure(self.PPFrame3,text = f"Status: {self.Gesture_Stat}", fg_color="#FF8157",text_color="black",font=("System", 20, "bold"))
                #     self.patient3_stat.grid(row=2, column=0, padx=20, pady=(20, 20))
                    
                #---------------------------------------------------------------------------------------------------------------------------------------------------------------------
                    
                sys.path.append('Behavior_Models/Fall Detection')
                from Fall_Detection import FallDetector
                
                self.Get_Fall_Stat = FallDetector()
                self.Fall_Stat, self.Fall_Frame =  self.Get_Fall_Stat.detect(Frame)
                # cv2.imshow('Fall Detection', self.Fall_Frame)
                print("Fall Detection: ",self.Fall_Stat)
                
                self.patient1_stat = customtkinter.CTkLabel(self.PPFrame1,text = f"Status: {self.Sleep_Stat,self.Eating_Stat}\nRequest: {self.Gesture_Stat}\nEmergency: {self.Fall_Stat}", fg_color="#B80E0E",text_color="black",font=("System", 20, "bold"))
                self.patient1_stat.grid(row=2, column=0, padx=20, pady=(20, 20))
                
                self.patient2_stat = customtkinter.CTkLabel(self.PPFrame2,text = f"Status: {self.Sleep_Stat,self.Eating_Stat}\nRequest: {self.Gesture_Stat}\nEmergency: {self.Fall_Stat}", fg_color="#B80E0E",text_color="black",font=("System", 20, "bold"))
                self.patient2_stat.grid(row=2, column=0, padx=20, pady=(20, 20))
                
                self.patient3_stat= customtkinter.CTkLabel(self.PPFrame3,text = f"Status: {self.Sleep_Stat,self.Eating_Stat}\nRequest: {self.Gesture_Stat}\nEmergency: {self.Fall_Stat}", fg_color="#B80E0E",text_color="black",font=("System", 20, "bold"))
                self.patient3_stat.grid(row=2, column=0, padx=20, pady=(20, 20))
        

        cap.release()
        cv2.destroyAllWindows()
                    

    def set_name(self):
        self.logo_label.configure(text=self.name)
        
    def Check_Credentials1(self):
        self.WarningLabel = customtkinter.CTkLabel(Main, text="Missing Fields...", font=customtkinter.CTkFont(size=20, weight="bold"), fg_color="red")

        if self.username_entry.get() == "":
            print("NOT ACCEPTED")
            self.username_entry.configure(bg_color="red")
            self.WarningLabel.place(x=Main.winfo_screenwidth()/2 - 510, y=Main.winfo_screenheight()/2 - 10, anchor="center")
            # userlabel = customtkinter.CTkLabel(Main, text="Username", font=("System", 40, "bold"), fg_color= "red")
            # userlabel.place(x=Main.winfo_screenwidth()/2 - 800, y=Main.winfo_screenheight()/2 - 400, anchor="center")
        if self.password_entry.get() == "":
            print("NOT ACCEPTED")
            self.password_entry.configure(bg_color="red")
            self.WarningLabel.place(x=Main.winfo_screenwidth()/2 - 510, y=Main.winfo_screenheight()/2 - 10, anchor="center")
            # passlabel = customtkinter.CTkLabel(Main, text="Password", font=("System", 40, "bold"), fg_color= "red")
            # passlabel.place(x=Main.winfo_screenwidth()/2 - 800, y=Main.winfo_screenheight()/2 - 250, anchor="center")
        if self.username_entry.get() == "211777" and self.password_entry.get() == "1235":
            self.start_model = True
            self.Get_Dashboard()
            # cam_thread.start()
        
            #CHECK SERVER FOR ACTUAL PASS STEVEN CRUD      
        

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
        self.login_button = customtkinter.CTkButton(self.login_frame, text="Login", command=lambda:self.Check_Credentials1(), width=200)
        self.login_button.grid(row=4, column=0, padx=30, pady=(15, 15))
        
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
        self.ContinueButton = customtkinter.CTkButton(Main, text="Continue", command=lambda: self.Continue(),  width=500, height=125, font=("System", 40, "bold"), fg_color="darkgreen")
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

