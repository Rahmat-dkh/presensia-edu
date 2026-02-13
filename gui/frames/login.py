import customtkinter as ctk
from database.db_handler import Database

class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, on_login_success, **kwargs):
        super().__init__(master, **kwargs)
        self.on_login_success = on_login_success
        self.db = Database()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Center Card
        self.card = ctk.CTkFrame(self, width=400, height=500, corner_radius=20, border_width=1, border_color=("gray80", "gray30"))
        self.card.grid(row=0, column=0, padx=20, pady=20)
        self.card.grid_propagate(False) # Keep size fixed

        # Brand / Logo Placeholder
        self.logo_label = ctk.CTkLabel(self.card, text="PRO", 
                                       font=ctk.CTkFont(size=40, weight="bold"),
                                       text_color=("#1f538d", "#5dade2"))
        self.logo_label.pack(pady=(50, 10))

        self.title_label = ctk.CTkLabel(self.card, text="Face Attendance Admin", 
                                        font=ctk.CTkFont(size=18, weight="normal"))
        self.title_label.pack(pady=(0, 40))

        # Inputs
        self.username_entry = ctk.CTkEntry(self.card, placeholder_text="Username", 
                                           width=300, height=45, corner_radius=10)
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self.card, placeholder_text="Password", 
                                           show="*", width=300, height=45, corner_radius=10)
        self.password_entry.pack(pady=10)

        # Login Button
        self.login_btn = ctk.CTkButton(self.card, text="Login to Dashboard", 
                                       command=self.login_event,
                                       width=300, height=45, corner_radius=10,
                                       font=ctk.CTkFont(size=14, weight="bold"))
        self.login_btn.pack(pady=(30, 20))

        self.error_label = ctk.CTkLabel(self.card, text="", text_color="#E74C3C")
        self.error_label.pack()

    def login_event(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        user = self.db.authenticate_user(username, password)
        if user:
            self.on_login_success(user)
        else:
            self.error_label.configure(text="Username atau Password salah!")
