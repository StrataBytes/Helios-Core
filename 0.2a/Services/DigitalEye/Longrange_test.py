from filelock import Timeout, FileLock
import cv2
import torch
import pandas as pd
import threading
import requests





"""NOTE: This is a test for the main_life_refined.py file. It is for detecting people from far distences"""

# Also note that this script is not hooked into the Core. It is simply a test for later integration.





lock_path = "/tmp/detect_humans_camera.lock"
lock = FileLock(lock_path)

with lock:
    print("[INFO|DS] YOLOv5 starting...")
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    print("[INFO|DS] YOLOv5 started!")

    camera_lock = threading.Lock()
    print("[INFO|DS] Locking Camera Access")
    print("[INFO|DS] Locking Complete")

    def detect_humans_camera():
        if not camera_lock.acquire(blocking=False):
            print("[ERR|DS] Webcam access is currently locked.")
            return

        try:
            cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
            if not cap.isOpened():
                print("\n[CRIT.ERR|DS] Cannot open webcam\n")
                return

            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            print("[INFO|DS] Webcam successfully opened.")

            while True:
                ret, frame = cap.read()
                if not ret:
                    print("\n[CRIT.ERR|DS] Failed to read frame from webcam\n")
                    break

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = model(frame_rgb)
                results = results.pandas().xyxy[0]
                results = results[results.confidence >= 0.4]

                detected = any(row['name'] == 'person' for index, row in results.iterrows())
                emotion = 'veryHappy' if detected else 'happy'
                print("===============Detection Service to Core===================")
                print(f"[INFO|DS] Detected {emotion}, sending data.")
                response = requests.post('http://localhost:5000/update_emotion', json={'emotion': emotion})
                print(f"[INFO|DS] Server response: {response.text}")
                print("===========================================================\n")



                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("[INFO|DS] Quit signal received, closing detection loop.")
                    break

        finally:
            cap.release()
            camera_lock.release()
            print("[INFO|DS] Webcam and lock released.")
            cv2.destroyAllWindows()

    if __name__ == "__main__":
        detect_humans_camera()
