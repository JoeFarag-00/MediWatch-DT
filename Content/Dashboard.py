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