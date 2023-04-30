import cv2
import time
from emotion_detector import emotionDetector
from sussy import Sussy

cap = cv2.VideoCapture(0)
emotion_detector = emotionDetector()
sus = Sussy()

status = 0
p_time = 0

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

    if status == 1:
        frame = emotion_detector.detect(frame=frame)
    elif status == 2:
        frame = sus.interact(cap=cap, frame=frame)

    cv2.putText(frame, f"FPS: {round(fps)}", (20, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)
    cv2.imshow("Image", frame)

    key = cv2.waitKey(1)

    if key == ord("a"):
        status = 0
    elif key == ord("b"):
        status = 1
    elif key == ord("c"):
        status = 2
    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
