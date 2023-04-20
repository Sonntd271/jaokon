import pygame

def play_sound(note,octave):
    pygame.init()
    print(f"playing {note}{octave}")
    pygame.mixer.music.load(f"piano-mp3/piano-mp3/{note}{octave}.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.quit()