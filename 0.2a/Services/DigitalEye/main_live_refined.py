from filelock import Timeout, FileLock
import cv2
import torch
import pandas as pd
import threading
import requests




"""Detection Service [DS]"""

#This is the code for human detection! 


#TODO: Integrate motion guesters. (wave, come here, ect.)
#TODO: Better Integration w/ front-end emotion screen (Usr feedback). Example, if a person is to the left, make the face look left. 
#TODO: Fork this service to activly look for people with lowest confidence to detect right away for after hours school.








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
                    print("\n[CRIT.ERR|DS] Failed to read frame from webcam\n(Camera Fail - Cannot use detection functionality.)")
                    break

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = model(frame_rgb)
                results = results.pandas().xyxy[0]
                results = results[results.confidence >= 0.5]#confidence. add or remove.

                #filter based on bounding box size. this is used to reduce false positives, and detection from people half across the school
                min_area = 30000  #minimum area to consider a detection valid
                results = results[(results.xmax - results.xmin) * (results.ymax - results.ymin) > min_area]

                for index, row in results.iterrows():
                    if row['name'] == 'person':
                        cv2.rectangle(frame, (int(row['xmin']), int(row['ymin'])), (int(row['xmax']), int(row['ymax'])), (0, 255, 0), 2)

                detected = any(row['name'] == 'person' for index, row in results.iterrows())
                emotion = 'veryHappy' if detected else 'happy'
                #print("===============Detection Service to Core===================")
                print(f"[INFO|DS] Detected {emotion}, sending data.")
                response = requests.post('http://localhost:5000/update_emotion', json={'emotion': emotion})
                #print(f"[INFO|DS] Server response: {response.text}")
                #print("===========================================================\n")

                #cv2.imshow("Detection Window", frame)

                # if cv2.waitKey(1) & 0xFF == ord('q'):
                #     print("[INFO|DS] Quit signal received, closing detection loop.")
                #     break

        finally:
            cap.release()
            camera_lock.release()
            print("[INFO|DS] Webcam and lock released.")
            cv2.destroyAllWindows()

    if __name__ == "__main__":
        detect_humans_camera()
