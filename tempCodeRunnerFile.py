import pygame
from sys import exit
import math
import settings,entities



pygame.init()

#window initialization
screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
pygame.display.set_caption("Top Down Shooter")
clock = pygame.time.Clock()

#load images


#creating sprites
moving_sprites =pygame.sprite.Group()
player = entities.Player()

while True:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    player.update()
    screen.fill((0,0,0))
    screen.blit(player.image, player.rect)

    pygame.draw.rect(screen , "red", player.hitbox_rect, width = 2)
    pygame.draw.rect(screen , "red", player.rect, width = 2)
    pygame.display.update()   
    clock.tick(settings.FPS)
