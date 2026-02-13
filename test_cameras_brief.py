import cv2
import os
from dotenv import load_dotenv

load_dotenv()
indices = []
for i in range(5):
    cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
    if cap.isOpened():
        ret, _ = cap.read()
        if ret: indices.append(i)
        cap.release()

print(f"ENV_VAL:{os.getenv('CAMERA_INDEX')}")
print(f"FOUND_INDICES:{indices}")
