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

gestures = {0:"do",1:"re",2:"mi",3:"fa",4:"sol",5:"la",6:"ti"}
model = load_model("data/doremi.h5",compile= False)
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
              loss=tf.keras.losses.BinaryCrossentropy(),
              metrics=[tf.keras.metrics.BinaryAccuracy(),
                       tf.keras.metrics.FalseNegatives()])

def music_game(index,cap,song,frame,bool):
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
    return inc,end

def choose_song():
    song,notes = [[],[]]
    with open("songs.json") as json_file:
        data = json.load(json_file)
        song = random.choice(list(data["songs"].items()))[1]
        notes = random.choice(list(data["notes"].items()))[1]
    return song,notes

def play_sound(note,octave):
    pygame.init()
    print(f"playing {note}{octave}")
    pygame.mixer.music.load(f"piano-mp3/piano-mp3/{note}{octave}.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.quit()

def parallel(note):
    octave = note[1]
    note = note[0]
    thread = threading.Thread(target = play_sound,args = (note,octave))
    thread.start()

def playback(song):
    pygame.init()
    for i in song:
        pygame.mixer.music.load(f"piano-mp3/piano-mp3/{i}.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    pygame.quit()

def hands_feed():
    HT = HandTracking()

    count = 0
    index = 0
    color = (0, 0, 255)

    # capture from live web cam
    cap = cv2.VideoCapture(0)
    frame_width, frame_height = int(cap.get(3)), int(cap.get(4))

    song,notes = choose_song()
    pred = "No predictions"
    prev_pred = None
    l = []
    
    while cap.isOpened():
        insert = False
        ret, frame = cap.read()

        if not ret:
            print("Ignoring empty camera frame.")
            continue

        image = frame.copy()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # hand tracking
        hands_results = HT.track(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # init frame each loop
        HT.read_results(image, hands_results)

        l = []
        if hands_results.multi_hand_landmarks:
            HT.draw_hand()
            HT.draw_hand_label()

            hand = hands_results.multi_hand_landmarks[0]
            for i in range(21):
                l += HT.get_moy_coords(hand, i)

            # sl = ",".join(map(str, l))
            # print(sl)
        else: 
            pred = "No predictions"

        print(l)

        if len(l) == 0:
            pred = ""
        else:
            a = [l]
            p = model.predict(a)    
            p_index = np.argmax(p, axis=1)
            pred = gestures[int(str(p_index)[1:-1])]
        
        # print("prev pred:", prev_pred)
        # print("pred:",pred)
        if prev_pred == pred and pred != "" and pred == song[index]:
            count += 1
            if count >= 7:
                color = (0,255,0)
                count = 0
                insert = True
        else:
            count = 0
            prev_pred = None
            color = (0,0,255)

        if pred != "No predictions":
            prev_pred = pred

        print(pred)
        print(insert)
        print(index)
        inc,end = music_game(index,cap,song,image,insert)

        if inc:
            parallel(notes[index])
            index += 1

        if end:
            playback(notes)
            #add stuff for resetting

        cv2.putText(image, pred, (10, frame_height - 10), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    color, 2)

        cv2.imshow("image", image)

        key = cv2.waitKey(100)

        if key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__== "__main__":
    hands_feed()
    