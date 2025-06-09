import pygame
import json
import settings
import math


entities_stuffs = json.load(open(r".\locations.json", "r"))


class Player(pygame.sprite.Sprite) :
    def __init__(self):
        super().__init__()

        self.idle_frames = [pygame.transform.rotozoom(pygame.image.load(path).convert_alpha(), 0, 0.35) for path in entities_stuffs["player"]["idle"]]
        self.idle_frame_index = 0
        self.idle_animation_time = 200  # milliseconds per frame
        self.last_idle_update = pygame.time.get_ticks()

        self.move_frames = [pygame.transform.rotozoom(pygame.image.load(path).convert_alpha(), 0, 0.35) for path in entities_stuffs["player"]["move"]]
        self.move_frame_index = 0
        self.move_animation_time = 100
        self.last_move_update = pygame.time.get_ticks()



        self.player_sprite = self.idle_frames[0]
        self.base_player_sprite = self.player_sprite
        self.hitbox_rect = self.base_player_sprite.get_rect(center = self.pos)
        self.rect = self.hitbox_rect.copy()
        self.pos = pygame.math.Vector2(settings.PLAYER_START_X, settings.PLAYER_START_Y)
        self.speed = settings.PLAYER_SPEED

        
        

    def user_input(self):
        self.velocity_x = 0 
        self.velocity_y = 0


        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity_x = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity_x = self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.velocity_y = -self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.velocity_y = self.speed
        
        if self.velocity_x != 0 and self.velocity_y != 0: # moving diagonally
            self.velocity_x /= math.sqrt(2)
            self.velocity_y /= math.sqrt(2)
    
    def player_turning(self): 
        self.mouse_coords = pygame.mouse.get_pos() 

        self.x_change_mouse_player = (self.mouse_coords[0] - (settings.WIDTH // 2))
        self.y_change_mouse_player = (self.mouse_coords[1] - (settings.HEIGHT // 2))
        self.angle = int(math.degrees(math.atan2(self.y_change_mouse_player, self.x_change_mouse_player)))
        self.angle = (self.angle) % 360 # if this stop working add 360 in the brackets

        self.image = pygame.transform.rotate(self.player_sprite, -self.angle)
        self.rect = self.image.get_rect(center = self.rect.center)

    def update(self):
        
        self.user_input()
        self.pos.x += self.velocity_x
        self.pos.y += self.velocity_y

        
        if self.velocity_x == 0 and self.velocity_y == 0:
            # Idle: animate idle frames
            now = pygame.time.get_ticks()
            if now - self.last_idle_update > self.idle_animation_time:
                self.idle_frame_index = (self.idle_frame_index + 1) % len(self.idle_frames)
                self.last_idle_update = now
            self.player_sprite = self.idle_frames[self.idle_frame_index]
        else :
            now = pygame.time.get_ticks()
            if now - self.last_move_update > self.move_animation_time:
                self.move_frame_index = (self.move_frame_index + 1) % len(self.move_frames)
                self.last_move_update = now
            self.player_sprite = self.move_frames[self.move_frame_index]

        self.player_turning()