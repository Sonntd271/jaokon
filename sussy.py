from getdata.HandTracking import HandTracking
import cv2
import tensorflow as tf
from keras.models import load_model
import numpy as np
import random
import pygame
import json
import time
import threading

SONG_FILE = "songs.json"


class Sussy:

    def __init__(self):
        
        self.gestures = {0: "do", 1: "re", 2: "mi", 3: "fa", 4: "sol", 5: "la", 6: "ti"}
        self.count = 0
        self.index = 0
        self.color = (0, 0, 255)
        self.pred = "No"
        self.prev_pred = None

        self.model = load_model("models/doremi.h5", compile=False)
        self.model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
                    loss=tf.keras.losses.BinaryCrossentropy(),
                    metrics=[tf.keras.metrics.BinaryAccuracy(),
                            tf.keras.metrics.FalseNegatives()])
        self.ht = HandTracking()
        self.choose_song()

    def music_game(self, index, cap, song, frame, bool):

        end = False
        inc = False
        cv2.putText(frame, song[index], (int(cap.get(3)/2), int(cap.get(4)/2)), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0,0,255), 2)
        if bool == True:
            index += 1
            inc = True
        if index == len(song):
            end = True
            index = 0
            print("END")

        return inc, end

    def choose_song(self):

        self.song, self.notes = [[], []]
        with open(SONG_FILE) as json_file:
            data = json.load(json_file)
            self.song = random.choice(list(data["songs"].items()))[1]
            self.notes = random.choice(list(data["notes"].items()))[1]

    def play_sound(self, note, octave):

        pygame.init()
        print(f"playing {note}{octave}")
        pygame.mixer.music.load(f"notes/{note}{octave}.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            # Check the tick
            pygame.time.Clock().tick(10)
        pygame.quit()

    def parallel(self, note):
        
        octave = note[1]
        note = note[0]
        thread = threading.Thread(target=self.play_sound, args=(note, octave))
        thread.start()

    def playback(self, song):

        pygame.init()
        for i in song:
            pygame.mixer.music.load(f"notes/{i}.mp3")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        pygame.quit()

    def interact(self, cap, frame):

        self.insert = False

        img = frame.copy()
        rgb_frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        rgb_frame.flags.writeable = False

        self.hands_results = self.ht.track(rgb_frame)
        
        rgb_frame.flags.writeable = True
        bgr_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)

        self.ht.read_results(bgr_frame, self.hands_results)
        
        l = []
        if self.hands_results.multi_hand_landmarks:
            self.ht.draw_hand()
            self.ht.draw_hand_label()

            hand = self.hands_results.multi_hand_landmarks[0]
            for i in range(21):
                l += self.ht.get_moy_coords(hand, i)
        else: 
            self.pred = "No"
        
        # print(l)

        if len(l) == 0:
            self.pred = ""
        else:
            a = [l]
            p = self.model.predict(a)    
            p_index = np.argmax(p, axis=1)
            self.pred = self.gestures[int(str(p_index)[1:-1])]
        
        if self.prev_pred == self.pred and self.pred != "" and self.pred == self.song[self.index]:
            self.count += 1
            if self.count >= 7:
                self.color = (0,255,0)
                self.count = 0
                self.insert = True
        else:
            self.count = 0
            self.prev_pred = None
            self.color = (0,0,255)

        if self.pred != "":
            self.prev_pred = self.pred
        
        print("Want:", self.song[self.index])
        print("Pred:", self.pred)
        print("Prev:", self.prev_pred)
        print("Count:", self.count)
        print("Insert:", self.insert)
        print("Index:", self.index)

        inc, end = self.music_game(self.index, cap, self.song, bgr_frame, self.insert)

        if inc:
            self.parallel(self.notes[self.index])
            self.index += 1

        if end:
            self.playback(self.notes)
            #add stuff for resetting
        
        cv2.putText(bgr_frame, self.pred, (10, int(cap.get(4)) - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, self.color, 2)

        return bgr_frame


if __name__== "__main__":
    
    cap = cv2.VideoCapture(0)
    sus = Sussy()

    while cap.isOpened():
        # insert = False
        ret, frame = cap.read()

        if not ret:
            print("Ignoring empty camera frame.")
            continue

        frame = sus.interact(cap=cap, frame=frame)

        cv2.imshow("Image", frame)

        if cv2.waitKey(1) == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows
    