import cv2
import time
import json
from emotion_detector import emotionDetector
from sussy import Sussy

CURRENT_STATUS_PATH = "statics/currentStatus.json"

def update_json(status_no):
    msg = {
        "status": status_no,
        "face": "",
        "note": ""
    }
    msg_json = json.dumps(msg, indent=4)

    with open(file=CURRENT_STATUS_PATH, mode="w") as current_status:
        current_status.write(msg_json)

cap = cv2.VideoCapture(0)
emotion_detector = emotionDetector()
sus = Sussy()

idle_ords = [ord("1"), ord("2"), ord("3"), ord("a")]
interaction_ords = [ord("4"), ord("5"), ord("7"), ord("8"), ord("b")]
music_ords = [ord("6"), ord("9"), ord("+"), ord("-"), ord("c")]

status = 0
p_time = 0
off_count = 0

while True:

    # Find haar cascade to draw bounding box around face
    ret, frame = cap.read()
    frame = cv2.resize(frame, (680, 480))

    c_time = time.time()
    fps = 1 / (c_time - p_time)
    p_time = c_time

    # Uncomment below to see device status
    # print(status)
    
    if not ret:
        print("Ignoring empty camera frame.")
        break

    if status == 0:
        update_json(status_no=status)
    elif status == 1:
        frame = emotion_detector.detect(frame=frame)
    elif status == 2:
        frame = sus.interact(cap=cap, frame=frame)

    cv2.putText(frame, f"FPS: {round(fps)}", (20, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)
    cv2.imshow("Image", frame)

    key = cv2.waitKey(1)
    # print(f"Key: {key}, Off count: {off_count}")

    if key in idle_ords:
        status = 0
        off_count += 1
    elif key in interaction_ords:
        status = 1
        off_count = 0
    elif key in music_ords:
        status = 2
        off_count = 0
        sus.choose_song()
    elif key == ord("q"):
        break
    else:
        off_count = 0

    if off_count >= 7:
        update_json(status_no=3)
        print("Turning off")
        break

cap.release()
cv2.destroyAllWindows()
