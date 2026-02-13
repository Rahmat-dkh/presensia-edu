import customtkinter as ctk
import os
from PIL import Image

from gui.frames.dashboard import DashboardFrame
from gui.frames.attendance import AttendanceFrame
from gui.frames.students import StudentsFrame
from gui.frames.reports import ReportsFrame
from gui.frames.login import LoginFrame

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Presensia Edu - Sistem Absensi Wajah Pintar")
        self.geometry("1100x650")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # create frames
        self.dashboard_frame = DashboardFrame(self, corner_radius=0, fg_color="transparent")
        self.attendance_frame = AttendanceFrame(self, corner_radius=0, fg_color="transparent")
        self.students_frame = StudentsFrame(self, corner_radius=0, fg_color="transparent")
        self.reports_frame = ReportsFrame(self, corner_radius=0, fg_color="transparent")
        
        # create navigation frame
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=("#F0F2F5", "#1A1C1E"))
        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="  PRESENSIA EDU", 
                                                 text_color=("#1f538d", "#5dade2"),
                                                 compound="left", font=ctk.CTkFont(size=18, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=30)

        self.dashboard_button = ctk.CTkButton(self.navigation_frame, corner_radius=8, height=45, border_spacing=12, text="   Dashboard",
                                               fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                               anchor="w", font=ctk.CTkFont(size=14), command=self.dashboard_button_event)
        self.dashboard_button.grid(row=1, column=0, sticky="ew", padx=15, pady=2)

        self.attendance_button = ctk.CTkButton(self.navigation_frame, corner_radius=8, height=45, border_spacing=12, text="   Attendance",
                                                fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                anchor="w", font=ctk.CTkFont(size=14), command=self.attendance_button_event)
        self.attendance_button.grid(row=2, column=0, sticky="ew", padx=15, pady=2)

        self.students_button = ctk.CTkButton(self.navigation_frame, corner_radius=8, height=45, border_spacing=12, text="   Students",
                                              fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                              anchor="w", font=ctk.CTkFont(size=14), command=self.students_button_event)
        self.students_button.grid(row=3, column=0, sticky="ew", padx=15, pady=2)

        self.reports_button = ctk.CTkButton(self.navigation_frame, corner_radius=8, height=45, border_spacing=12, text="   Reports",
                                             fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                             anchor="w", font=ctk.CTkFont(size=14), command=self.reports_button_event)
        self.reports_button.grid(row=4, column=0, sticky="ew", padx=15, pady=2)

        self.appearance_mode_menu = ctk.CTkOptionMenu(self.navigation_frame, values=["Dark", "Light", "System"],
                                                        font=ctk.CTkFont(size=12),
                                                        command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=7, column=0, padx=20, pady=20, sticky="s")

        # Login Frame
        self.login_frame = LoginFrame(self, on_login_success=self.on_login_success, corner_radius=0, fg_color=("#FFFFFF", "#121212"))
        self.login_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

    def on_login_success(self, user):
        self.login_frame.grid_forget()
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(6, weight=1)
        self.select_frame_by_name("dashboard")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.dashboard_button.configure(fg_color=("#D1D5DB", "#374151") if name == "dashboard" else "transparent")
        self.attendance_button.configure(fg_color=("#D1D5DB", "#374151") if name == "attendance" else "transparent")
        self.students_button.configure(fg_color=("#D1D5DB", "#374151") if name == "students" else "transparent")
        self.reports_button.configure(fg_color=("#D1D5DB", "#374151") if name == "reports" else "transparent")

        # Camera lifecycle management
        if name == "attendance":
            self.attendance_frame.start_camera()
        else:
            self.attendance_frame.stop_camera()

        # Update student list if students
        if name == "students":
            self.students_frame.refresh_student_list()
            self.students_frame.start_preview()
        else:
            self.students_frame.stop_preview()

        # show selected frame
        if name == "dashboard":
            self.dashboard_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.dashboard_frame.grid(row=0, column=1, sticky="nsew") # Workaround for display
            self.dashboard_frame.grid_forget()
        
        if name == "attendance":
            self.attendance_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.attendance_frame.grid_forget()
            
        if name == "students":
            self.students_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.students_frame.grid_forget()
            
        if name == "reports":
            self.reports_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.reports_frame.grid_forget()

    def dashboard_button_event(self):
        self.select_frame_by_name("dashboard")

    def attendance_button_event(self):
        self.select_frame_by_name("attendance")

    def students_button_event(self):
        self.select_frame_by_name("students")

    def reports_button_event(self):
        self.select_frame_by_name("reports")

    def change_appearance_mode_event(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)

    def dashboard_button_event(self):
        self.select_frame_by_name("dashboard")

    def attendance_button_event(self):
        self.select_frame_by_name("attendance")

    def students_button_event(self):
        self.select_frame_by_name("students")

    def reports_button_event(self):
        self.select_frame_by_name("reports")

    def change_appearance_mode_event(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)

if __name__ == "__main__":
    app = App()
    app.mainloop()
