import pygame
from sys import exit
import math
import settings
from entities import Player, NormalEnemy, BruteEnemy
from pytmx.util_pygame import load_pygame
from tiles import Tile
from random import randint
from camera import Camera
from stuffs import Bullet
from pathfinding import mark_wall
from timer import ElapsedTimer
from waves import waves, spawn_wave
pygame.init()

#window initialization
screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
pygame.display.set_caption("Top Down Shooter")
clock = pygame.time.Clock()

#load map
tmx_data = load_pygame(r"C:\Users\oldem\Desktop\MTC_Level\map.tmx")


#initializing grid of the map
grid_width = tmx_data.width
grid_height = tmx_data.height
grid = [[0 for _ in range(grid_height)] for _ in range(grid_width)]

#map setup
global map_width, map_height

map_width = tmx_data.width * tmx_data.tilewidth
map_height = tmx_data.height * tmx_data.tileheight

map_surface = pygame.Surface((map_width, map_height))

sprite_group =  pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()

#constants
ZOOM = 0.5


#creating sprites
moving_sprites =pygame.sprite.Group()
player = Player()
moving_sprites.add(player)


#creating camera
camera_group = Camera(player = player,zoom = ZOOM)
camera_group.add(*moving_sprites)
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
        mark_wall(grid=grid, grid_height=grid_height, grid_width=grid_width, tile_object=obj, tile_height= tmx_data.tileheight, tile_width = tmx_data.tilewidth)
        wall_rect.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        scaled_image = pygame.transform.scale(obj.image, (int(obj.width), int(obj.height)))
        camera_group.add(Tile(pos = (obj.x, obj.y), surf = scaled_image, groups = sprite_group))

#Will change
enemy_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()

                 
#timer
game_timer = ElapsedTimer()

#game state
current_wave = -1
max_waves = len(waves)
game_state = "playing"


while True:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    if game_state == "playing" and len(enemy_group) == 0:
        current_wave += 1
        if current_wave < max_waves:
            player.health = settings.PLAYER_HEALTH # refill health
            spawn_wave(current_wave, enemy_group,   camera_group)
        else:
            game_state = "win"
    
    if game_state in ("win", "game_over"):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key ==    pygame.K_r:
                # Reset everything
                current_wave = 0
                player.lives = 3
                player.health = player.max_health
                player.respawn()
                spawn_wave(current_wave, enemy_group,   camera_group)
                game_state = "playing"

    if game_state == "win":
        pass
    # Draw "You Win! Press R to restart"
    elif game_state == "game_over":
        pass
    # Draw "Game Over! Press R to restart"

    player.update(wall_rect=wall_rect, bullet_group=bullet_group, camera_group=camera_group)
    bullet_group.update(map_width = map_width, map_height=map_height, wall_rect = wall_rect)
    grenade_group.update(player = player, explosion_group = explosion_group, camera_group = camera_group)
    explosion_group.update()
    
    for enemy in enemy_group :
        if isinstance(enemy, BruteEnemy) :
            enemy.update(player = player, wall_rect =  wall_rect, camera_group = camera_group, grenade_group=grenade_group, bullet_group = bullet_group, tmx_data=tmx_data, grid = grid)
            
        else :
            enemy.update(player = player, wall_rect =  wall_rect, camera_group = camera_group, bullet_group = bullet_group, tmx_data=tmx_data, grid = grid)
        pygame.draw.rect(screen, (255, 0, 0), enemy.rect, 2)
    
    screen.fill((0,0,0))
    camera_group.draw(screen)
    player.draw_health_bar(screen, 20, 20, 200, 20)
    player.draw_lives_counter(surface = screen, x= 20,  y =50)
    player.draw_waves_counter(surface = screen,current_wave= current_wave+1, x =20, y = 80)
    
    font = pygame.font.SysFont(None, 36)
    elapsed_seconds = game_timer.get_elapsed()
    minutes = elapsed_seconds // 60
    seconds = elapsed_seconds % 60
    timer_text = font.render(f"Time: {minutes:02}:{seconds:02}", True, (255,255,255))
    screen.blit(timer_text, (20, 120))

    if player.damage_overlay_alpha > 0:
        damage_overlay = pygame.Surface((settings.WIDTH, settings.HEIGHT), pygame.SRCALPHA)
        damage_overlay.fill((255, 0, 0, int(player. damage_overlay_alpha)))  # RGBA
        screen.blit(damage_overlay, (0, 0))


    pygame.display.update()
    clock.tick(settings.FPS)
