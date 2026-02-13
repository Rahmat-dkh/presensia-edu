import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
from core.face_logic import FaceEngine
from core.logger import Logger
from database.db_handler import Database
from datetime import datetime
import os
import threading
import time

class AttendanceFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.face_engine = FaceEngine()
        self.db = Database()
        self.logger = Logger()
        
        # Configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header Container
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        
        self.header = ctk.CTkLabel(self.header_frame, text="Sistem Presensi Wajah", font=ctk.CTkFont(size=26, weight="bold"))
        self.header.pack(side="left")

        self.btn_switch_cam = ctk.CTkButton(self.header_frame, text="🔄 Ganti Kamera", width=120, height=32,
                                           command=self.switch_camera_event, fg_color="#34495E", hover_color="#2C3E50")
        self.btn_switch_cam.pack(side="right", padx=10)

        # Main Content: Camera
        self.cam_container = ctk.CTkFrame(self, corner_radius=15, border_width=2, border_color=("gray80", "gray30"))
        self.cam_container.grid(row=1, column=0, padx=40, pady=10, sticky="nsew")
        self.cam_container.grid_columnconfigure(0, weight=1)
        self.cam_container.grid_rowconfigure(0, weight=1)

        self.video_label = ctk.CTkLabel(self.cam_container, text="Memuat Kamera...", font=ctk.CTkFont(size=14))
        self.video_label.grid(row=0, column=0, sticky="nsew", padx=4, pady=4)

        # Bottom Info Bar
        self.info_frame = ctk.CTkFrame(self, height=80, corner_radius=10, fg_color=("gray85", "gray20"))
        self.info_frame.grid(row=2, column=0, padx=40, pady=(10, 30), sticky="ew")

        self.info_label = ctk.CTkLabel(self.info_frame, text="Status: Menunggu Deteksi", font=ctk.CTkFont(size=16, weight="bold"))
        self.info_label.pack(expand=True, pady=15)

        # Check for dependency
        from core.face_logic import FACE_REC_AVAILABLE
        if not FACE_REC_AVAILABLE:
            self.info_label.configure(text="Library 'face_recognition' tidak ditemukan!", text_color="#E74C3C")

        self.cap = None
        self.is_running = False
        self.last_recognition_time = {} # For cooldown

    def switch_camera_event(self):
        """Cycle through camera indices 0, 1, 2."""
        current_idx = int(os.getenv('CAMERA_INDEX', 0))
        new_idx = (current_idx + 1) % 4 # Cycle up to 3
        
        # Update .env in memory and file if possible
        os.environ['CAMERA_INDEX'] = str(new_idx)
        self.stop_camera()
        self.after(500, self.start_camera)

    def start_camera(self):
        if not self.is_running:
            self.info_label.configure(text="Menghubungkan ke Kamera... (Sabar ya)", text_color="#3498DB")
            # Run camera opening in a separate thread to prevent UI hang
            thread = threading.Thread(target=self._open_camera_task, daemon=True)
            thread.start()

    def _open_camera_task(self):
        try:
            cam_idx = int(os.getenv('CAMERA_INDEX', 0))
            cap = cv2.VideoCapture(cam_idx, cv2.CAP_DSHOW)
            
            # Allow some time for driver to respond
            start_time = time.time()
            while not cap.isOpened() and time.time() - start_time < 5:
                time.sleep(0.5)

            if cap.isOpened():
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                self.cap = cap
                self.is_running = True
                self.face_engine.load_known_faces()
                self.after(0, self.update_frame)
                self.after(0, lambda: self.info_label.configure(text="Status: Kamera Aktif", text_color="#2ECC71"))
            else:
                self.after(0, lambda: self.info_label.configure(
                    text=f"Gagal: Kamera {cam_idx} tidak merespon. Cek Iriun Anda!", 
                    text_color="#E74C3C"
                ))
        except Exception as e:
            self.after(0, lambda: self.info_label.configure(text=f"Error: {str(e)}", text_color="#E74C3C"))

    def stop_camera(self):
        self.is_running = False
        if self.cap:
            self.cap.release()

    def update_frame(self):
        if self.is_running:
            ret, frame = self.cap.read()
            if not ret:
                self.video_label.configure(text="Gagal mengambil gambar dari kamera!", image="")
                return

            # Mirror frame for intuitive feeling
            frame = cv2.flip(frame, 1)
            
            # Recognition logic
            results = self.face_engine.recognize_faces(frame)
            
            for res in results:
                top, right, bottom, left = res['box']
                name = res['name']
                conf = res['confidence']
                
                # Modern Box (Green for recognized, Red for unknown)
                color = (46, 204, 113) if name != "Unknown" else (231, 76, 60) # BGR
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                
                # Background for text
                cv2.rectangle(frame, (left, top - 35), (right, top), color, cv2.FILLED)
                cv2.putText(frame, f"{name}", (left + 6, top - 10), 
                            cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 1)

                # Mark Attendance if recognized
                if name != "Unknown" and conf > 0.5:
                    self.process_attendance(res, frame)

            # Convert to PIL for Tkinter
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb_frame)
            
            # Resize keeping aspect ratio
            w, h = img.size
            target_w = 720
            target_h = int((h / w) * target_w)
            
            img_tk = ctk.CTkImage(light_image=img, dark_image=img, size=(target_w, target_h))
            self.video_label.configure(image=img_tk, text="")
        
        self.after(20, self.update_frame)

    def process_attendance(self, result, frame):
        student_id = result['id']
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")
        
        # Save proof screenshot
        proof_dir = "assets/proofs"
        if not os.path.exists(proof_dir): os.makedirs(proof_dir)
        proof_path = f"{proof_dir}/{student_id}_{now.strftime('%Y%m%d_%H%M%S')}.jpg"
        
        # Log to DB (UNIQUE constraint handles duplicates per day)
        success = self.db.log_attendance(student_id, date_str, time_str, proof_path)
        if success and success.rowcount > 0:
            cv2.imwrite(proof_path, frame)
            self.info_label.configure(text=f"Berhasil: {result['name']} mencatat kehadiran!", text_color="green")
            self.logger.info(f"Attendance recorded for {result['name']} ({student_id})")
