import pygame
import json
import settings
import math


entities_stuffs = json.load(open(r".\locations.json", "r"))


class Player(pygame.sprite.Sprite) :
    def __init__(self):
        super().__init__()

        self.idle_frames = [pygame.transform.rotozoom(pygame.image.load(path).convert_alpha(), 0, settings.PLAYER_SIZE) for path in entities_stuffs["player"]["idle"]]
        self.idle_frame_index = 0
        self.idle_animation_time = 200  # milliseconds per frame
        self.last_idle_update = pygame.time.get_ticks()

        self.move_frames = [pygame.transform.rotozoom(pygame.image.load(path).convert_alpha(), 0, settings.PLAYER_SIZE) for path in entities_stuffs["player"]["move"]]
        self.move_frame_index = 0
        self.move_animation_time = 100
        self.last_move_update = pygame.time.get_ticks()


        self.pos = pygame.math.Vector2(settings.PLAYER_START_X, settings.PLAYER_START_Y)

        self.image = self.idle_frames[0]
        self.base_sprite = self.image

        self.hitbox_rect = self.base_sprite.get_rect(center = self.pos)
        self.rect = self.hitbox_rect.copy()
        self.speed = settings.PLAYER_SPEED

        
        
    def move(self, wall_rect):
        #Move in X first 
        self.pos.x += self.velocity_x
        self.hitbox_rect.centerx = self.pos.x

        

        for wall in wall_rect:
            if self.hitbox_rect.colliderect(wall):
                if self.velocity_x > 0:  # moving right
                    self.hitbox_rect.right = wall.left
                elif self.velocity_x < 0:  # moving left
                    self.hitbox_rect.left = wall.right
                self.pos.x = self.hitbox_rect.centerx

        #Move in Y
        self.pos.y += self.velocity_y
        self.hitbox_rect.centery = self.pos.y
        
        for wall in wall_rect:
            if self.hitbox_rect.colliderect(wall):
                if self.velocity_y > 0:  # moving down
                    self.hitbox_rect.bottom = wall.top
                elif self.velocity_y < 0:  # moving up
                    self.hitbox_rect.top = wall.bottom
                self.pos.y = self.hitbox_rect.centery
        

        self.rect.center = self.hitbox_rect.center
        # self.check_collision("horizontal")

        # self.check_collision("vertical")

        
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
        mouse_x, mouse_y = pygame.mouse.get_pos() 
        screen_center = pygame.display.get_surface().get_rect().center

        

        #getting the angle -> theta = tan-1(change in y / change in x)
        self.x_change_mouse_player = (mouse_x - (screen_center[0]))
        self.y_change_mouse_player = (mouse_y - (screen_center[1]))
        self.angle = math.degrees(math.atan2(self.y_change_mouse_player, self.x_change_mouse_player))

        self.image = pygame.transform.rotate(self.base_sprite, -self.angle)
        
        self.rect = self.image.get_rect(center = self.hitbox_rect.center)
        
    def update(self, wall_rect):
        
        self.user_input()
        self.move(wall_rect = wall_rect)
        
        
        self.rect.center = (int(self.pos.x), int(self.pos.y))
        
        if self.velocity_x == 0 and self.velocity_y == 0:
            # Idle: animate idle frames
            now = pygame.time.get_ticks()
            if now - self.last_idle_update > self.idle_animation_time:
                self.idle_frame_index = (self.idle_frame_index + 1) % len(self.idle_frames)
                self.last_idle_update = now
            self.base_sprite = self.idle_frames[self.idle_frame_index]
        else :
            now = pygame.time.get_ticks()
            if now - self.last_move_update > self.move_animation_time:
                self.move_frame_index = (self.move_frame_index + 1) % len(self.move_frames)
                self.last_move_update = now
            self.base_sprite = self.move_frames[self.move_frame_index]

        
        self.player_turning()