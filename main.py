import pygame
from sys import exit
import math
import settings,entities
from pytmx.util_pygame import load_pygame
import tiles
from random import randint

pygame.init()

#window initialization
screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
pygame.display.set_caption("Top Down Shooter")
clock = pygame.time.Clock()

#load map
tmx_data = load_pygame(r"C:\Users\oldem\Desktop\MTC_Level\map.tmx")
map_surface = pygame.Surface((tmx_data.width * tmx_data.tilewidth,
                              tmx_data.height * tmx_data.tileheight))
sprite_group =  pygame.sprite.Group()

for layer in tmx_data.visible_layers:
    if hasattr(layer, 'data'):
        for x,y,surf in layer.tiles():
            pos = (x*128, y*128)
            tiles.Tile(pos = pos, surf = surf, groups = sprite_group)


#creating camera
camera_group = pygame.sprite.Group()


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
    sprite_group.draw(screen)
    screen.blit(player.image, player.rect)

    pygame.draw.rect(screen , "red", player.hitbox_rect, width = 2)
    pygame.draw.rect(screen , "red", player.rect, width = 2)
    pygame.display.update()   
    clock.tick(settings.FPS)
