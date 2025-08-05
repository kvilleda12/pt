"""
Capture.py handles capturing frames every 20 seconds
"""

# capture.py
import cv2 as cv
import time
from visual_reasoning import process_frame
from session_manager import log_caption

CAPTURE_INTERVAL = 20  # seconds
SESSION_DURATION = 30 * 60  # 30 minutes

def start_capture():
    cap = cv.VideoCapture(0)
    start_time = time.time()
    last_capture = 0

    while time.time() - start_time < SESSION_DURATION:
        ret, frame = cap.read()
        if not ret:
            break

        current_time = time.time()
        if current_time - last_capture >= CAPTURE_INTERVAL:
            caption = process_frame(frame)
            log_caption(caption)
            last_capture = current_time

        cv.imshow('Live Feed', frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    start_capture()
