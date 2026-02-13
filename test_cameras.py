import cv2
import os
from dotenv import load_dotenv

def test_cameras():
    load_dotenv()
    env_idx = os.getenv('CAMERA_INDEX', 'Not Set')
    print(f"Current Dashboard Settings:")
    print(f"CAMERA_INDEX in .env: {env_idx}")
    print("-" * 30)
    print("Mencari kamera yang tersedia...")
    
    working_indices = []
    # Test first 10 indices
    for i in range(10):
        # Use CAP_DSHOW on Windows for better compatibility with virtual cams
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        if cap.isOpened():
            # Get camera properties if possible
            ret, _ = cap.read()
            if ret:
                print(f"Kamera ditemukan pada INDEX: {i} (SIAP DIGUNAKAN)")
                working_indices.append(i)
            else:
                print(f"Kamera ditemukan pada INDEX: {i} (Terbuka tapi tidak ada gambar)")
            cap.release()
    
    if not working_indices:
        print("TIDAK ADA KAMERA ditemukan!")
    else:
        print("-" * 30)
        print(f"Saran: Jika kamera laptop adalah 0, maka kamera HP biasanya adalah {working_indices[1] if len(working_indices) > 1 else 'indeks berikutnya'}.")

if __name__ == "__main__":
    test_cameras()
