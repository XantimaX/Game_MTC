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


#map setup
map_width = tmx_data.width * tmx_data.tilewidth
map_height = tmx_data.height * tmx_data.tileheight
map_surface = pygame.Surface((map_width, map_height))

sprite_group =  pygame.sprite.Group()


#constants
ZOOM = 0.5


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






while True:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


    #creating camera
    camera_offset = pygame.Vector2(
        player.pos.x - (settings.WIDTH / (2 * ZOOM)),
        player.pos.y - (settings.HEIGHT / (2 * ZOOM))
    )
    player.update(wall_rect=wall_rect, camera_offset=camera_offset, zoom=ZOOM)
    


    # for wall in wall_rect:
    #     pygame.draw.rect(screen, "red", wall, 2)
    sprite_group.draw(map_surface)
    moving_sprites.draw(map_surface)

    
    for wall in wall_rect:
        pygame.draw.rect(map_surface, "red", wall, 2)

    scaled_surface = pygame.transform.smoothscale(map_surface, (int(map_width * ZOOM), int(map_height * ZOOM)))
    scaled_camera_offset = (camera_offset * ZOOM)

    screen.fill((0,0,0))
    screen.blit(scaled_surface, (-scaled_camera_offset.x, -scaled_camera_offset.y))
   
    pygame.display.update()  


    clock.tick(settings.FPS)
