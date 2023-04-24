import cv2
import json
import numpy as np
from keras.models import model_from_json

MODEL_PATH_JSON = 'models/emotion_model.json'
MODEL_PATH_WEIGHTS = "models/emotion_model.h5"
CURRENT_STATUS_PATH = "statics/currentStatus.json"
TARGET_COUNT = 20


class emotionDetector:

    def __init__(self):

        self.emotion_dict = {0: "angry", 1: "disgusted", 2: "fearful", 3: "happy", 4: "neutral", 5: "sad", 6: "surprised"}
        self.count = 0
        self.prev_pred = None

        # load json and create model
        json_file = open(MODEL_PATH_JSON, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        self.emotion_model = model_from_json(loaded_model_json)

        # load weights into new model
        self.emotion_model.load_weights(MODEL_PATH_WEIGHTS)
        print("Loaded model from disk")

        self.face_detector = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_detection.xml')

    def update_json(self, emotion):

        msg = {
            "status": 1,
            "face": emotion,
            "note": ""
        }
        msg_json = json.dumps(msg, indent=4)
        
        print(f"Sending {emotion}")
        with open(file=CURRENT_STATUS_PATH, mode="w") as current_status:
            current_status.write(msg_json)
        print(f"Sent successfully")

        self.count = 0
        print(f"Resetting count, count: {self.count}")
    
    def detect(self, frame):

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # detect faces available on camera
        num_faces = self.face_detector.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

        # take each face available on the camera and Preprocess it
        for (x, y, w, h) in num_faces:
            cv2.rectangle(frame, (x, y - 50), (x + w, y + h + 10), (0, 255, 0), 4)
            roi_gray_frame = gray_frame[y:y + h, x:x + w]
            cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray_frame, (48, 48)), -1), 0)

            # predict the emotions
            self.emotion_prediction = self.emotion_model.predict(cropped_img)
            maxindex = int(np.argmax(self.emotion_prediction))
            emotion = self.emotion_dict[maxindex]

            if emotion == self.prev_pred and self.prev_pred != None:
                self.count += 1
                if self.count >= TARGET_COUNT:
                    print(f"Count reached {self.count}, generating json")
                    self.update_json(emotion=emotion)
            
            self.prev_pred = emotion
            cv2.putText(frame, emotion, (x + 5, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

        return frame


if __name__ == "__main__":
    
    # start the webcam feed
    cap = cv2.VideoCapture(0)
    emotion_detector = emotionDetector()

    while True:

        # Find haar cascade to draw bounding box around face
        ret, frame = cap.read()
        frame = cv2.resize(frame, (680, 480))
        if not ret:
            break
        
        frame = emotion_detector.detect(frame=frame)

        cv2.imshow('Emotion Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()