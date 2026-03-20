import pygame
import time

pygame.mixer.init()
pygame.mixer.music.load("hi_test.mp3")
pygame.mixer.music.play()

print("Playing...")
while pygame.mixer.music.get_busy():
    time.sleep(0.2)

print("Done")
pygame.mixer.quit()