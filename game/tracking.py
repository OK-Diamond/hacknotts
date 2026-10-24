import cv2


class FaceTracker:
    def __init__(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index)
        base = cv2.data.haarcascades
        self.face_cascade = cv2.CascadeClassifier(base + "haarcascade_frontalface_default.xml")
        self.eye_cascade = cv2.CascadeClassifier(base + "haarcascade_eye.xml")
        self.frame = None       # latest RGB frame for pygame
        self.face_box = None    # (x, y, w, h) or None
        self.eyes_open = False  # used for blinking later

    def update(self):
        """Grab a frame and look for a face. Returns True if one is seen."""
        ok, frame = self.cap.read()
        if not ok:
            return False
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = self.face_cascade.detectMultiScale(
            gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100)
        )

        self.face_box = None
        self.eyes_open = False
        if len(faces) > 0:
            x, y, w, h = max(faces, key=lambda f: f[2] * f[3])  # biggest face
            self.face_box = (x, y, w, h)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # look for eyes in the upper half of the face only
            upper_face = gray[y : y + h // 2, x : x + w]
            eyes = self.eye_cascade.detectMultiScale(upper_face, 1.1, 8, minSize=(20, 20))
            self.eyes_open = len(eyes) >= 1

        self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return self.face_box is not None

    def release(self):
        self.cap.release()