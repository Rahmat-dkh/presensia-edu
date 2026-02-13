try:
    import face_recognition
    FACE_REC_AVAILABLE = True
except ImportError:
    FACE_REC_AVAILABLE = False

import cv2
import numpy as np
import json
from database.db_handler import Database

class FaceEngine:
    def __init__(self):
        self.db = Database()
        self.known_face_encodings = []
        self.known_face_names = []
        self.known_student_ids = []
        if FACE_REC_AVAILABLE:
            self.load_known_faces()

    def load_known_faces(self):
        """Load all student faces from database into memory."""
        if not FACE_REC_AVAILABLE:
            return
            
        students = self.db.get_all_students()
        self.known_face_encodings = []
        self.known_face_names = []
        self.known_student_ids = []

        for student in students:
            if student['face_encoding']:
                encoding = np.array(json.loads(student['face_encoding']))
                self.known_face_encodings.append(encoding)
                self.known_face_names.append(student['name'])
                self.known_student_ids.append(student['student_id'])

    def recognize_faces(self, frame):
        """
        Detect and recognize faces in the given frame.
        Returns a list of dicts: [{'name': ..., 'id': ..., 'box': ..., 'confidence': ...}]
        """
        if not FACE_REC_AVAILABLE:
            return []
            
        # Scale down for speed, but use RGB for quality
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Detect face locations using higher accuracy model (HOG is default, use CNN if GPU available)
        face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        results = []
        for face_encoding, face_location in zip(face_encodings, face_locations):
            # tolerance 0.5 is more strict than 0.6, prevents false positives
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, tolerance=0.5)
            name = "Unknown"
            student_id = None
            confidence = 0

            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]
                    student_id = self.known_student_ids[best_match_index]
                    confidence = 1 - face_distances[best_match_index]

            # Scale back up 2x (since we resized by 0.5)
            top, right, bottom, left = face_location
            top, right, bottom, left = top * 2, right * 2, bottom * 2, left * 2
            
            results.append({
                'name': name,
                'id': student_id,
                'box': (top, right, bottom, left),
                'confidence': float(confidence)
            })
        
        return results

    def get_encoding_from_image(self, frame):
        """Get face encoding from a single frame with image enhancement."""
        if not FACE_REC_AVAILABLE:
            return None
            
        # Image Enhancement: Auto-brightness and contrast (CLAHE)
        # This helps a lot if the camera is grainy or the room is dim
        try:
            lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
            cl = clahe.apply(l)
            limg = cv2.merge((cl,a,b))
            enhanced_frame = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
        except:
            enhanced_frame = frame # Fallback

        rgb_frame = cv2.cvtColor(enhanced_frame, cv2.COLOR_BGR2RGB)
        
        # Use full resolution for registration (no downscaling) for maximum detail
        face_locations = face_recognition.face_locations(rgb_frame, number_of_times_to_upsample=2)
        
        if len(face_locations) > 0:
            # Pick the largest face
            if len(face_locations) > 1:
                face_locations.sort(key=lambda x: (x[2]-x[0])*(x[1]-x[3]), reverse=True)
            
            encodings = face_recognition.face_encodings(rgb_frame, [face_locations[0]])
            if len(encodings) > 0:
                return json.dumps(encodings[0].tolist())
                
        return None
