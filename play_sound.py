import pygame
import json
import random 
def play_sound(note):
    pygame.init()
    pygame.mixer.music.load(f"piano-mp3/piano-mp3/{note}.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(1)
    pygame.quit()

with open("songs.json") as json_file:
    data = json.load(json_file)
    notes = random.choice(list(data["notes"].items()))[1]
    for note in notes:
        play_sound(note)