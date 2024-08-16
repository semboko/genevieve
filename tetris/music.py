import pygame


pygame.init()

casual_music = pygame.mixer.Sound("./Casual 8-bit.wav")
casual_music.set_volume(0)
explosion = pygame.mixer.Sound("./explosion.wav")
casual_music.play(loops=-1)
