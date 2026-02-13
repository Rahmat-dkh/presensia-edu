import customtkinter as ctk
from database.db_handler import Database
from core.face_logic import FaceEngine
import cv2
from PIL import Image, ImageTk
import os
import time
import threading

class StudentsFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.db = Database()
        self.face_engine = FaceEngine()
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

        self.header = ctk.CTkLabel(self.header_frame, text="Manajemen Data Siswa", font=ctk.CTkFont(size=20, weight="bold"))
        self.header.pack(side="left")

        self.btn_switch_cam = ctk.CTkButton(self.header_frame, text="🔄 Ganti Kamera", width=120, height=32,
                                           command=self.switch_camera_event, fg_color="#34495E", hover_color="#2C3E50")
        self.btn_switch_cam.pack(side="right")

        # Main Layout (Split View)
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.main_container.grid_columnconfigure(0, weight=3) # Table
        self.main_container.grid_columnconfigure(1, weight=2) # Form

        # Left: Student List (Simplified placeholder)
        self.table_frame = ctk.CTkScrollableFrame(self.main_container, label_text="Daftar Siswa")
        self.table_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self.refresh_student_list()

        # Right: Add Student Form
        self.form_frame = ctk.CTkFrame(self.main_container)
        self.form_frame.grid(row=0, column=1, sticky="nsew")
        
        ctk.CTkLabel(self.form_frame, text="Tambah Siswa Baru", font=ctk.CTkFont(weight="bold")).pack(pady=10)
        
        self.id_entry = ctk.CTkEntry(self.form_frame, placeholder_text="NIS / ID Siswa")
        self.id_entry.pack(pady=5, padx=20, fill="x")
        
        self.name_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Nama Lengkap")
        self.name_entry.pack(pady=5, padx=20, fill="x")
        
        self.class_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Kelas (contoh: 10-A)")
        self.class_entry.pack(pady=5, padx=20, fill="x")

        self.reg_video_label = ctk.CTkLabel(self.form_frame, text="Kamera Preview", height=220, 
                                          fg_color=("#E1E4E8", "#24292E"), corner_radius=10)
        self.reg_video_label.pack(pady=10, padx=20, fill="x")

        self.btn_capture = ctk.CTkButton(self.form_frame, text="Ambil Foto & Simpan", command=self.capture_and_save)
        self.btn_capture.pack(pady=10, padx=20, fill="x")
        
        self.status_label = ctk.CTkLabel(self.form_frame, text="")
        self.status_label.pack(pady=5)

        self.cap = None
        self.is_preview_running = False

    def switch_camera_event(self):
        """Cycle through camera indices 0, 1, 2, 3."""
        current_idx = int(os.getenv('CAMERA_INDEX', 0))
        new_idx = (current_idx + 1) % 4
        os.environ['CAMERA_INDEX'] = str(new_idx)
        self.stop_preview()
        self.after(500, self.start_preview)

    def start_preview(self):
        if not self.is_preview_running:
            self.status_label.configure(text="Memulai Kamera...", text_color="#3498DB")
            thread = threading.Thread(target=self._open_preview_task, daemon=True)
            thread.start()

    def _open_preview_task(self):
        try:
            cam_idx = int(os.getenv('CAMERA_INDEX', 0))
            cap = cv2.VideoCapture(cam_idx, cv2.CAP_DSHOW)
            
            start_time = time.time()
            while not cap.isOpened() and time.time() - start_time < 5:
                time.sleep(0.5)

            if cap.isOpened():
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                self.cap = cap
                self.is_preview_running = True
                self.after(0, self.update_preview)
                self.after(0, lambda: self.status_label.configure(text="Preview Aktif", text_color="#2ECC71"))
            else:
                self.after(0, lambda: self.status_label.configure(text=f"Kamera {cam_idx} tidak merespon!", text_color="#E74C3C"))
        except Exception as e:
            self.after(0, lambda: self.status_label.configure(text=f"Error Preview: {str(e)}", text_color="#E74C3C"))

    def stop_preview(self):
        self.is_preview_running = False
        if self.cap:
            self.cap.release()
            self.cap = None

    def update_preview(self):
        if self.is_preview_running and self.cap:
            ret, frame = self.cap.read()
            if not ret:
                self.reg_video_label.configure(text="Kamera terputus / Sibuk", image="")
                return
                
            # Mirror for preview
            frame = cv2.flip(frame, 1)
            
            # Draw a guide box for the face
            h, w, _ = frame.shape
            cv2.rectangle(frame, (w//4, h//4), (3*w//4, 3*h//4), (255, 255, 255), 1)

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb_frame)
            img_tk = ctk.CTkImage(light_image=img, dark_image=img, size=(300, 225))
            self.reg_video_label.configure(image=img_tk, text="")
        
        self.after(20, self.update_preview)

    def refresh_student_list(self):
        for child in self.table_frame.winfo_children():
            child.destroy()
        
        students = self.db.get_all_students()
        for i, s in enumerate(students):
            ctk.CTkLabel(self.table_frame, text=f"{s['student_id']} - {s['name']} ({s['class_name']})", anchor="w").pack(fill="x", padx=10, pady=2)

    def capture_and_save(self):
        sid = self.id_entry.get()
        name = self.name_entry.get()
        cls = self.class_entry.get()
        
        if not sid or not name:
            self.status_label.configure(text="ID & Nama harus diisi!", text_color="#E74C3C")
            return

        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                # Check for face encoding
                encoding = self.face_engine.get_encoding_from_image(frame)
                if encoding:
                    # Create directory if missing
                    profile_dir = "assets/profiles"
                    if not os.path.exists(profile_dir): os.makedirs(profile_dir)
                    
                    photo_path = f"{profile_dir}/{sid}.jpg"
                    cv2.imwrite(photo_path, frame)
                    
                    success = self.db.add_student(sid, name, cls, encoding, photo_path)
                    if success:
                        self.status_label.configure(text="BERHASIL: Siswa Terdaftar!", text_color="#2ECC71", font=ctk.CTkFont(weight="bold"))
                        self.id_entry.delete(0, 'end')
                        self.name_entry.delete(0, 'end')
                        self.class_entry.delete(0, 'end')
                        self.refresh_student_list()
                    else:
                        self.status_label.configure(text="ERROR: Database failure!", text_color="#E74C3C")
                else:
                    self.status_label.configure(text="Wajah TIDAK terdeteksi! Coba lebih dekat.", text_color="#E74C3C", font=ctk.CTkFont(weight="bold"))
            else:
                self.status_label.configure(text="Kamera Error!", text_color="#E74C3C")
