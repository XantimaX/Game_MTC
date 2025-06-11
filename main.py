import pygame
from sys import exit
import math
import settings,entities
from pytmx.util_pygame import load_pygame
from tiles import Tile
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


#constants
ZOOM = 1


wall_rect = []

tile_w = tmx_data.tilewidth
tile_h = tmx_data.tileheight
scaled_tile_w = int(tile_w * ZOOM)
scaled_tile_h = int(tile_h * ZOOM)


for layer in tmx_data.layers:
    if hasattr(layer, "data") :
        for x,y,surf in layer.tiles():
            pos = (x*128, y*128)
            Tile(pos = pos, surf = surf, groups = sprite_group)

for obj in tmx_data.objects:
    if obj.name == "wall":
        wall_rect.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        scaled_image = pygame.transform.scale(obj.image, (int(obj.width), int(obj.height)))
        Tile(pos = (obj.x, obj.y), surf = scaled_image, groups = sprite_group)
        


#constants
ZOOM = 0.5

#creating sprites
moving_sprites =pygame.sprite.Group()
player = entities.Player()
moving_sprites.add(player)

#creating camera





while True:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    player.update(wall_rect)
    


    # for wall in wall_rect:
    #     pygame.draw.rect(screen, "red", wall, 2)
    sprite_group.draw(screen)
    moving_sprites.draw(screen)

    for wall in wall_rect:
        pygame.draw.rect(screen, "red", wall, 2)

    pygame.display.update()  

    clock.tick(settings.FPS)
