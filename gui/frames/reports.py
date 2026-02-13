import customtkinter as ctk
from core.export_logic import ExcelExporter
import os

class ReportsFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.exporter = ExcelExporter()
        
        self.grid_columnconfigure(0, weight=1)

        self.header = ctk.CTkLabel(self, text="Laporan Kehadiran", font=ctk.CTkFont(size=20, weight="bold"))
        self.header.grid(row=0, column=0, padx=20, pady=20)

        self.export_all_btn = ctk.CTkButton(self, text="Export Semua Data ke Excel", 
                                            command=self.export_all_data, height=50)
        self.export_all_btn.grid(row=1, column=0, padx=20, pady=10)

        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.grid(row=2, column=0, padx=20, pady=10)

    def export_all_data(self):
        success, msg = self.exporter.export_attendance()
        if success:
            self.status_label.configure(text=f"Berhasil diekspor: {msg}", text_color="green")
            # Open folder
            os.startfile(os.path.dirname(os.path.abspath(msg)))
        else:
            self.status_label.configure(text=msg, text_color="red")
