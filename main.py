import cv2
from emotion_detector import emotionDetector
from sussy import Sussy

cap = cv2.VideoCapture(0)
emotion_detector = emotionDetector()
sus = Sussy()

status = 0

while True:

    # Find haar cascade to draw bounding box around face
    ret, frame = cap.read()
    frame = cv2.resize(frame, (680, 480))

    print(status)
    
    if not ret:
        print("Ignoring empty camera frame.")
        break

    if cv2.waitKey(1) == ord("a"):
        status = 1
    elif cv2.waitKey(1) == ord("b"):
        status = 2

    if status == 1:
        frame = emotion_detector.detect(frame=frame)
    elif status == 2:
        frame = sus.interact(cap=cap, frame=frame)

    cv2.imshow("Image", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
