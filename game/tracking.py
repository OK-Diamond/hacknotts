import os
import time

import cv2
import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision

MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "face_landmarker.task")

CLOSE_THRESHOLD = 0.5   # blink score above this = eyes closed
OPEN_THRESHOLD = 0.3    # must drop below this to count as open again
COOLDOWN_SECONDS = 0.25  # ignore blinks closer together than this


class FaceTracker:
    def __init__(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index)

        options = vision.FaceLandmarkerOptions(
            base_options=mp_python.BaseOptions(model_asset_path=MODEL_PATH),
            running_mode=vision.RunningMode.VIDEO,
            num_faces=1,
            output_face_blendshapes=True,
        )
        self.landmarker = vision.FaceLandmarker.create_from_options(options)

        self.frame = None        # latest RGB frame for pygame
        self.face_box = None     # (x, y, w, h) or None
        self.eyes_open = True
        self.blinked = False     # True for exactly one frame when a blink starts
        self.blink_score = 0.0   # 0 = open, 1 = closed (handy for tuning)

        self._eyes_closed = False
        self._last_blink = 0.0
        self._last_ts = 0

    def update(self):
        """Grab a frame and look for a face. Returns True if a face is seen."""
        ok, frame = self.cap.read()
        if not ok:
            return False
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # timestamps must always increase
        ts = max(int(time.monotonic() * 1000), self._last_ts + 1)
        self._last_ts = ts
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        result = self.landmarker.detect_for_video(mp_image, ts)

        self.blinked = False
        self.face_box = None

        if result.face_landmarks:
            lms = result.face_landmarks[0]
            h, w, _ = rgb.shape
            xs = [lm.x * w for lm in lms]
            ys = [lm.y * h for lm in lms]
            x0, y0, x1, y1 = int(min(xs)), int(min(ys)), int(max(xs)), int(max(ys))
            self.face_box = (x0, y0, x1 - x0, y1 - y0)
            cv2.rectangle(rgb, (x0, y0), (x1, y1), (0, 255, 0), 2)

            scores = {b.category_name: b.score for b in result.face_blendshapes[0]}
            self.blink_score = (scores["eyeBlinkLeft"] + scores["eyeBlinkRight"]) / 2

            # hysteresis: closes above 0.5, only reopens below 0.3
            if not self._eyes_closed and self.blink_score > CLOSE_THRESHOLD:
                self._eyes_closed = True
                now = time.monotonic()
                if now - self._last_blink > COOLDOWN_SECONDS:
                    self.blinked = True
                    self._last_blink = now
            elif self._eyes_closed and self.blink_score < OPEN_THRESHOLD:
                self._eyes_closed = False

            self.eyes_open = not self._eyes_closed
        else:
            self._eyes_closed = False
            self.eyes_open = True
            self.blink_score = 0.0

        self.frame = rgb
        return self.face_box is not None

    def release(self):
        self.cap.release()
        self.landmarker.close()