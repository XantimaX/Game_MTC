import pygame
import settings

pygame.init()
pygame.mixer.init()

# Load sounds


# Load and play music

shoot_sound = pygame.mixer.Sound(settings.SHOOT_SOUND)
shoot_sound.set_volume(0.2)



def combat_song():
    pygame.mixer.music.load(r"Assets\music\bfg_10000.wav")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
def boss_song():
    pygame.mixer.music.load(r"Assets\music\boss_song.wav")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

def gameover_song():
    pygame.mixer.music.load(r"Assets\music\gameover.wav")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

def mainmenu_song():
    pygame.mixer.music.load(r"Assets\music\main_menu.wav")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

def game_win_song():
    pygame.mixer.music.load(r"Assets\music\game_win.wav")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)


