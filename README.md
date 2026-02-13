# Presensia Edu 🎓

**Presensia Edu** adalah sistem manajemen absensi sekolah modern yang berbasis teknologi pengenalan wajah (*face recognition*). Aplikasi ini dirancang untuk memberikan kemudahan, akurasi, dan kecepatan dalam mencatat kehadiran siswa menggunakan kamera standar atau kamera *smartphone* sebagai webcam.

## ✨ Fitur Utama
- **Presensi Wajah Real-Time**: Deteksi dan pengenalan wajah secara instan dengan feedback visual (bounding box hijau/merah).
- **Dashboard Statistik**: Pantau total siswa dan jumlah kehadiran hari ini secara visual.
- **Manajemen Siswa**: Tambah data siswa dengan pendaftaran wajah langsung melalui kamera.
- **Dukungan Multi-Kamera**: Fitur "Ganti Kamera" otomatis untuk berpindah antara webcam laptop dan kamera HP (Iriun/DroidCam).
- **Keamanan Admin**: Sistem login aman untuk melindungi data manajemen.
- **Laporan Excel**: Ekspor data kehadiran ke format Excel untuk keperluan administrasi.
- **Antarmuka Premium**: Desain modern menggunakan tema *Dark Mode* yang elegan.

## 🛠️ Teknologi yang Digunakan
- **Bahasa Pemrograman**: Python 3.x
- **GUI Framework**: CustomTkinter
- **Face Recognition**: library `face_recognition` (dlib) & OpenCV 
- **Database**: MySQL
- **Pengolahan Gambar**: Pillow, NumPy

## 🚀 Panduan Instalasi

### 1. Persyaratan Sistem
Pastikan Anda sudah menginstal:
- Python (Versi 3.8 ke atas)
- MySQL (Bisa menggunakan XAMPP atau Laragon)

### 2. Instalasi Library
Buka terminal/CMD dan jalankan perintah berikut:
```bash
pip install opencv-python face-recognition customtkinter mysql-connector-python pillow python-dotenv openpyxl pandas
```

### 3. Konfigurasi Database
1. Buat database baru di MySQL dengan nama `faceabsensi`.
2. Edit file `.env` dan sesuaikan dengan user/password MySQL Anda:
   ```env
   DB_HOST=localhost
   DB_USER=root
   DB_PASS=
   DB_NAME=faceabsensi
   CAMERA_INDEX=0
   ```
3. Jalankan skrip inisialisasi untuk membuat tabel otomatis:
   ```bash
   python database/init_db.py
   ```

### 4. Menjalankan Aplikasi
Setelah database siap, jalankan aplikasi utama:
```bash
python main.py
```

## 💡 Tips Penggunaan Kamera HP
Jika ingin menggunakan kamera HP (Samsung A55, dll) agar deteksi lebih akurat:
1. Hubungkan HP ke laptop menggunakan aplikasi **Iriun Webcam** atau **DroidCam**.
2. Di dalam aplikasi, klik tombol **🔄 Ganti Kamera** di pojok kanan atas hingga tampilan berganti ke kamera HP Anda.
3. Pastikan pencahayaan cukup agar fitur pengenalan wajah bekerja maksimal.

## 📝 Lisensi
Proyek ini dibuat untuk tujuan pendidikan dan manajemen sekolah yang efisien.

---
**Dibuat dengan ❤️ untuk Masa Depan Pendidikan Indonesia**
