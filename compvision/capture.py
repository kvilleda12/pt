import cv2 as cv
import time
from session_manager import start_session, log_caption, end_session
from visual_reasoning import process_frame
from db_interface import store_caption, store_summary
from llm_interface import summarize_captions

CAPTURE_INTERVAL = 20  # seconds
SESSION_DURATION = 30 * 60  # 30 minutes

def main():
    start_session(user_id="user_1")  # Adjust user_id as needed

    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    start_time = time.time()
    last_capture = 0

    while time.time() - start_time < SESSION_DURATION:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame.")
            break

        current_time = time.time()
        if current_time - last_capture >= CAPTURE_INTERVAL:
            caption = process_frame(frame)
            print(f"Caption: {caption}")
            log_caption(caption)
            store_caption(caption)  # save caption to DB or file
            last_capture = current_time

        cv.imshow('Live Feed', frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

    summary = end_session()
    print("Session Summary:")
    print(summary)

    

if __name__ == "__main__":
    main()
