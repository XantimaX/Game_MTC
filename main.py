import pygame
from sys import exit
import math
import settings,entities
from pytmx.util_pygame import load_pygame
from tiles import Tile
from random import randint
from camera import Camera

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


#creating sprites
moving_sprites =pygame.sprite.Group()
player = entities.Player()
moving_sprites.add(player)

#creating camera
camera_group = Camera(player = player,zoom = ZOOM)
camera_group.add(*moving_sprites)
print("Camera Group Sprites:", camera_group.sprites())
wall_rect = []

tile_w = tmx_data.tilewidth
tile_h = tmx_data.tileheight
scaled_tile_w = int(tile_w * ZOOM)
scaled_tile_h = int(tile_h * ZOOM)

for layer in tmx_data.layers:
    if hasattr(layer, "data") :
        for x,y,surf in layer.tiles():
            pos = (x*128, y*128)
            camera_group.add(Tile(pos = pos, surf = surf, groups = sprite_group))

for obj in tmx_data.objects:
    if obj.name == "wall":
        wall_rect.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        scaled_image = pygame.transform.scale(obj.image, (int(obj.width), int(obj.height)))
        camera_group.add(Tile(pos = (obj.x, obj.y), surf = scaled_image, groups = sprite_group))


while True:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    player.update(wall_rect=wall_rect)
    print(f"Player pos: {player.pos}, rect center: {player.rect.center}, hitbox: {player.hitbox_rect}")
    screen.fill((0,0,0))
    camera_group.draw(screen)


    pygame.display.update()
    clock.tick(settings.FPS)
