import customtkinter
import os
from tkinter import messagebox
from tkinter import filedialog
customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('green')
import re
from tkinter import Tk, Label, Text, Button, Menu
import random
from PIL import Image

class MainGUI():
    
    @staticmethod
    
    def DestroyAll():
        widgets = Main.winfo_children()
        for widget in widgets:
                widget.destroy()
                
    def Continue():
        MainGUI.DestroyAll()
        MainGUI.Login_Page()
    
    def ResetWindow():
        Main.destroy()
        os.startfile(r"MainGUI.py")
        
    def change_appearance_mode_event(new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
    
    def Get_Dashboard(username):
        MainGUI.DestroyAll()

        bots = None
        users = None
        sent_message = None
        received_message = None
        name = None
        message_counter = 1
        chat_counter = 2
        Main.resizable(width=False, height=False)
        Main.title("Dashboard")
        Main.geometry(f"{1100}x{510}")

        Main.grid_columnconfigure(1, weight=1)
        
        app_logo = customtkinter.CTkImage(light_image=Image.open("Assets\doctor.png"),
                                  size=(100, 100))

        sidebar_frame = customtkinter.CTkFrame(Main, width=140, corner_radius=0)
        sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        sidebar_frame.grid_rowconfigure(4, weight=1)
        logo = customtkinter.CTkLabel(sidebar_frame, image=app_logo, text="",
                                           font=customtkinter.CTkFont(size=20, weight="bold"))
        logo.grid(row=0, column=0, padx=20, pady=(20, 10))
        logo_label = customtkinter.CTkLabel(sidebar_frame, text="Chats",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        logo_label.grid(row=1, column=0, padx=20)
        sidebar_button_1 = customtkinter.CTkButton(sidebar_frame, text="Profile")
        sidebar_button_1.grid(row=2, column=0, padx=20, pady=10)

        appearance_mode_label = customtkinter.CTkLabel(sidebar_frame, text="Appearance Mode:", anchor="w")
        appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        appearance_mode_options = customtkinter.CTkOptionMenu(sidebar_frame,
                                                                   values=["Light", "Dark", "System"],
                                                                   command=MainGUI.change_appearance_mode_event)
        appearance_mode_options.grid(row=5, column=0, padx=20, pady=(10, 10))

        exit_button = customtkinter.CTkButton(sidebar_frame, text="Exit", hover_color="Red")
        exit_button.grid(row=6, column=0, padx=20, pady=10)

        tabview = customtkinter.CTkTabview(master=Main, width=250, height=490)
        tabview.grid(row=1, column=1, columnspan=2, padx=(20, 10), pady=(10, 0), sticky="nsew")

        tabview.add("View Patients") 
        tabview.set("View Patients")
        
        tabview.add("Register patients") 
        tabview.set("Register patients")
        
        tabview.add("Active Nurses") 
        tabview.set("Active Nurses")
        
        tabview.add("Settings") 
        tabview.set("Settings")

        MainGUI.set_name(username,logo_label)
    

    def set_name(name,logo_label):
        logo_label.configure(text=name)
        
    def Check_Credentials1(username,password,login_frame):
        WarningLabel = customtkinter.CTkLabel(Main, text="Missing Fields...", font=customtkinter.CTkFont(size=20, weight="bold"), fg_color="red")

        if username.get() == "":
            print("NOT ACCEPTED")
            username.configure(bg_color="red")
            WarningLabel.place(x=Main.winfo_screenwidth()/2 - 510, y=Main.winfo_screenheight()/2 - 10, anchor="center")
            # userlabel = customtkinter.CTkLabel(Main, text="Username", font=("System", 40, "bold"), fg_color= "red")
            # userlabel.place(x=Main.winfo_screenwidth()/2 - 800, y=Main.winfo_screenheight()/2 - 400, anchor="center")
        if password.get() == "":
            print("NOT ACCEPTED")
            password.configure(bg_color="red")
            WarningLabel.place(x=Main.winfo_screenwidth()/2 - 510, y=Main.winfo_screenheight()/2 - 10, anchor="center")
            # passlabel = customtkinter.CTkLabel(Main, text="Password", font=("System", 40, "bold"), fg_color= "red")
            # passlabel.place(x=Main.winfo_screenwidth()/2 - 800, y=Main.winfo_screenheight()/2 - 250, anchor="center")
        if username.get() == "mina" and password.get() == "wese5":
            MainGUI.Get_Dashboard("mina")
            #CHECK SERVER FOR ACTUAL PASS STEVEN CRUD      
        

    def GoBack_Home():
        MainGUI.DestroyAll()
        Main.geometry("700x580".format(ScreenWidth, ScreenHeight))
        MainGUI.Main_Screen()
        
    def Login_Page():
        MainGUI.DestroyAll()
    
        # global username, password
        # userLabel = customtkinter.CTkLabel(Main, text="Username", font=("System", 40, "bold"))
        # username = customtkinter.CTkEntry(Main, placeholder_text="Username",width=300, height=50)
        # passLabel = customtkinter.CTkLabel(Main, text="Password", font=("System", 40, "bold"))
        # password = customtkinter.CTkEntry(Main, placeholder_text="Password", width=300, height=50,show="*")
        
        # LoginBtn = customtkinter.CTkButton(Main, text="Login", width=150, height=60, font=("System", 40, "bold"), fg_color="darkgreen", command=lambda: MainGUI.Check_Credentials1(username,password,userLabel,passLabel))
        # Back_Btn = customtkinter.CTkButton(Main, text="<- Back",width=80, height=32, font=("System", 20, "bold"), fg_color="DarkRed", command=lambda:MainGUI.GoBack_Login())   

        # username.place(x=Main.winfo_screenwidth()/2 - 750,y=Main.winfo_screenheight()/2 - 330, anchor="center")
        # password.place(x=Main.winfo_screenwidth()/2 - 750,y=Main.winfo_screenheight()/2 - 180, anchor="center")

        # userLabel.place(x=Main.winfo_screenwidth()/2 - 800, y=Main.winfo_screenheight()/2 - 400, anchor="center")
        # passLabel.place(x=Main.winfo_screenwidth()/2 - 800, y=Main.winfo_screenheight()/2 - 250, anchor="center")

        # Back_Btn.place(x=Main.winfo_screenwidth()/2 - 880,y=Main.winfo_screenheight()/2 - 490, anchor="center")
        # LoginBtn.place(x=Main.winfo_screenwidth()/2 - 400,y=Main.winfo_screenheight() / 2 - 50, anchor="center")
        
        # current_path = os.path.dirname(os.path.realpath(__file__))
        # login_image = customtkinter.CTkImage(Image.open(current_path + "\Assets\medical-team.png"),size=(250, 250))
        # login_img_Label = customtkinter.CTkLabel(Main, image=login_image,text = "")
        # login_img_Label.place(x=Main.winfo_screenwidth()/2 - 420,y=Main.winfo_screenheight() / 2 - 250, anchor="center")
        #--------------------------------------------------------------------------------------------------------------------------------
        
        width = 900
        height = 600
        Main.geometry(f"{width}x{height}")
        Main.resizable(False, False)
        current_path = os.path.dirname(os.path.realpath(__file__))
        bg_image = customtkinter.CTkImage(Image.open(current_path + "/Assets/thumb-1920-638841.png"),size=(width, height))
        bg_image_label = customtkinter.CTkLabel(Main, image=bg_image)
        bg_image_label.grid(row=0, column=0)

        login_frame = customtkinter.CTkFrame(Main, corner_radius=0)
        login_frame.grid(row=0, column=0, sticky="ns")
        login_label = customtkinter.CTkLabel(login_frame, text="Patient-See\nLogin",
                                                  font=customtkinter.CTkFont(size=20, weight="bold"))
        
        current_path = os.path.dirname(os.path.realpath(__file__))
        login_image = customtkinter.CTkImage(Image.open(current_path + "\Assets\medical-team.png"),size=(200, 200))
        login_img_Label = customtkinter.CTkLabel(login_frame, image=login_image,text = "")
        
        
        login_label.grid(row=0, column=0, padx=30, pady=(40, 20))
        username_entry = customtkinter.CTkEntry(login_frame, width=200, placeholder_text="username")
        login_img_Label.grid(row=1, column=0, padx=30, pady=(15, 15))
        username_entry.grid(row=2, column=0, padx=30, pady=(15, 15))
        password_entry = customtkinter.CTkEntry(login_frame, width=200, show="*", placeholder_text="password")
        password_entry.grid(row=3, column=0, padx=30, pady=(0, 15))
        login_button = customtkinter.CTkButton(login_frame, text="Login", command=lambda:MainGUI.Check_Credentials1(username_entry,password_entry,login_frame), width=200)
        login_button.grid(row=4, column=0, padx=30, pady=(15, 15))
        
        Back_Btn = customtkinter.CTkButton(Main, text="<- Back",width=80, height=32, font=("System", 20, "bold"), fg_color="DarkRed", command=lambda:MainGUI.GoBack_Home())
        Back_Btn.place(x=Main.winfo_screenwidth()/2 - 880,y=Main.winfo_screenheight()/2 - 490, anchor="center")


    def Main_Screen():
        MainGUI.DestroyAll()
        WelcomeLabel = customtkinter.CTkLabel(Main, text="Patient-See", font=("System", 40, "bold"))
        ContinueButton = customtkinter.CTkButton(Main, text="Continue", command=lambda: MainGUI.Continue(),  width=500, height=125, font=("System", 40, "bold"), fg_color="darkgreen")
        QuitButton = customtkinter.CTkButton(Main, text="Quit", command=quit, width=500, height=125, font=("System", 40, "bold"), fg_color="darkgreen")
        WelcomeLabel.place(x=ScreenWidth/2-610, y=ScreenHeight/2 - 450, anchor="center")
        ContinueButton.place(x=ScreenWidth/2 - 610, y=ScreenHeight/2 - 250, anchor="center")
        QuitButton.place(x=ScreenWidth/2 - 610, y=ScreenHeight/2 - 100, anchor="center")

        

Main = customtkinter.CTk()
Main.title("Patient-See")
Main.attributes("-topmost", True)

ScreenWidth = Main.winfo_screenwidth()
ScreenHeight = Main.winfo_screenheight()
Main.geometry("700x580".format(ScreenWidth, ScreenHeight))

MainGUI.Main_Screen()
Main.mainloop()
