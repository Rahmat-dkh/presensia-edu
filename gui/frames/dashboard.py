import customtkinter as ctk
from database.db_handler import Database

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.db = Database()
        self.grid_columnconfigure((0, 1, 2), weight=1)

        # Title
        self.title_label = ctk.CTkLabel(self, text="Dashboard Statistik", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, columnspan=3, padx=20, pady=(20, 10), sticky="w")

        # Stats Cards
        self.stats_container = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_container.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        self.stats_container.grid_columnconfigure((0, 1, 2), weight=1)

        self.total_students_card = self.create_stat_card("Total Siswa", "0", 0, 0, ("#3498DB", "#2980B9"))
        self.present_today_card = self.create_stat_card("Hadir Hari Ini", "0", 0, 1, ("#2ECC71", "#27AE60"))
        self.late_today_card = self.create_stat_card("Izin / Terlambat", "0", 0, 2, ("#F1C40F", "#F39C12"))

        # Recent Activity Table Placeholder
        self.activity_label = ctk.CTkLabel(self, text="Aktivitas Terakhir", font=ctk.CTkFont(size=18, weight="bold"))
        self.activity_label.grid(row=2, column=0, columnspan=3, padx=20, pady=(20, 10), sticky="w")
        
        self.activity_frame = ctk.CTkScrollableFrame(self, height=300)
        self.activity_frame.grid(row=3, column=0, columnspan=3, padx=20, pady=10, sticky="nsew")

        self.update_stats()

    def create_stat_card(self, title, value, row, col, color_theme):
        card = ctk.CTkFrame(self.stats_container, corner_radius=15, fg_color=color_theme)
        card.grid(row=row, column=col, padx=15, pady=10, sticky="nsew")
        
        lbl_title = ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=15, weight="normal"), text_color="white")
        lbl_title.pack(pady=(15, 5))
        
        lbl_value = ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=36, weight="bold"), text_color="white")
        lbl_value.pack(pady=(0, 20))
        return lbl_value

    def update_stats(self):
        # Update Cards
        total, present = self.db.get_todays_stats()
        self.total_students_card.configure(text=str(total))
        self.present_today_card.configure(text=str(present))
        
        # Update Activity Table
        for child in self.activity_frame.winfo_children():
            child.destroy()
            
        activities = self.db.get_recent_activity(10)
        
        # Headers
        header_frame = ctk.CTkFrame(self.activity_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(header_frame, text="Waktu", width=100, anchor="w", font=ctk.CTkFont(weight="bold")).pack(side="left")
        ctk.CTkLabel(header_frame, text="Nama Siswa", width=250, anchor="w", font=ctk.CTkFont(weight="bold")).pack(side="left")
        ctk.CTkLabel(header_frame, text="Kelas", width=100, anchor="w", font=ctk.CTkFont(weight="bold")).pack(side="left")
        ctk.CTkLabel(header_frame, text="Status", width=100, anchor="w", font=ctk.CTkFont(weight="bold")).pack(side="left")

        for act in activities:
            row = ctk.CTkFrame(self.activity_frame, fg_color=("gray90", "gray25"), corner_radius=5)
            row.pack(fill="x", padx=5, pady=2)
            
            waktu = str(act['attendance_time'])
            ctk.CTkLabel(row, text=waktu, width=100, anchor="w").pack(side="left", padx=5)
            ctk.CTkLabel(row, text=act['name'], width=250, anchor="w").pack(side="left", padx=5)
            ctk.CTkLabel(row, text=act['class_name'], width=100, anchor="w").pack(side="left", padx=5)
            
            status_color = "green" if act['status'] == "Present" else "orange"
            ctk.CTkLabel(row, text=act['status'], width=100, anchor="w", text_color=status_color).pack(side="left", padx=5)
