import pygame
import json
import settings
import math
from bullet import Bullet
from pathfinding import world_to_grid, astar
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

        #shooting
        self.shoot = False
        self.shoot_cooldown = 0
        
        
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

        
    def user_input(self, bullet_group, camera_group):
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
        
        if pygame.mouse.get_pressed() == (1,0,0) or keys[pygame.K_SPACE] :
            self.shoot = True
            self.is_shooting(bullet_group = bullet_group, camera_group = camera_group)
        else :
            self.shoot = False

    
    def player_turning(self): 
        mouse_x, mouse_y = pygame.mouse.get_pos() 
        screen_center = pygame.display.get_surface().get_rect().center

        

        #getting the angle -> theta = tan-1(change in y / change in x)
        self.x_change_mouse_player = (mouse_x - (screen_center[0]))
        self.y_change_mouse_player = (mouse_y - (screen_center[1]))
        self.angle = math.degrees(math.atan2(self.y_change_mouse_player, self.x_change_mouse_player))

        self.image = pygame.transform.rotate(self.base_sprite, -self.angle)
        
        self.rect = self.image.get_rect(center = self.hitbox_rect.center)
    
    #method for shooting
    def is_shooting(self, bullet_group, camera_group):
        if self.shoot_cooldown == 0 :
            self.shoot_cooldown = settings.PLAYER_SHOOT_COOLDOWN
            self.bullet = Bullet(pos = self.pos, angle = self.angle)    
            bullet_group.add(self.bullet)
            camera_group.add(self.bullet)


    def update(self, wall_rect, bullet_group, camera_group):
        
        self.user_input(bullet_group=bullet_group, camera_group = camera_group, )
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
            
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        self.player_turning()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.transform.rotozoom(
            pygame.image.load(settings.NORMAL_ENEMY_IMAGE).convert_alpha(), 0, settings.NORMAL_ENEMY_SIZE
        )

        self.base_sprite = self.image

        self.pos = pygame.math.Vector2(pos)
        self.hitbox_rect = self.base_sprite.get_rect(center = self.pos)
        self.rect = self.hitbox_rect.copy()

        self.speed = settings.NORMAL_ENEMY_SPEED
        self.health = settings.NORMAL_ENEMY_HEALTH
        self.shoot_cooldown = 0

        #path finding shenanigans
        self.path = []
        self.last_grid_pos = None
        self.last_player_grid_pos = None

    def turn_towards_player(self, player):
        player_x, player_y = player.pos
        enemy_x , enemy_y = self.pos
        

        #getting the angle -> theta = tan-1(change in y / change in x)
        dx = (enemy_x - player_x)
        dy = (enemy_y-player_y)
        self.angle = math.degrees(math.atan2(dy, dx))

        self.image = pygame.transform.rotate(self.base_sprite, -(self.angle + 90))
        
        self.rect = self.image.get_rect(center=(int(self.pos.x), int(self.pos.y)))

    def shoot_at_player(self, player, bullet_group, camera_group):
        if self.shoot_cooldown == 0:
            # Calculate angle to player
            dx = player.pos.x - self.pos.x
            dy = player.pos.y - self.pos.y
            angle = math.degrees(math.atan2(dy, dx))
            # Create and add bullet
            bullet = Bullet(pos=self.pos, angle=angle)
            bullet_group.add(bullet)
            camera_group.add(bullet)
            # Set cooldown (e.g., 30 frames for half a second at 60 fps)
            self.shoot_cooldown = settings.ENEMY_SHOOT_COOLDOWN
        
    def update(self, player, wall_rect, bullet_group, camera_group, grid, tmx_data):
        # Simple AI: move toward player
        
        tilewidth,tileheight = tmx_data.tilewidth, tmx_data.tileheight
        enemy_grid = world_to_grid(pos = self.pos, tileheight= tileheight, tilewidth=tilewidth)
        player_grid = world_to_grid(pos = player.pos, tileheight= tileheight, tilewidth=tilewidth)
        
        if enemy_grid != self.last_grid_pos or player_grid != self.last_player_grid_pos or not self.path:
            self.path = astar(grid, enemy_grid, player_grid)
            self.last_grid_pos = enemy_grid
            self.last_player_grid_pos = player_grid

        
        direction = pygame.math.Vector2(player.pos) - self.pos

        if self.path and len(self.path) > 1:
            next_cell = self.path[1]  # path[0] is current cell
            target_x = next_cell[0] * tilewidth + tilewidth // 2
            target_y = next_cell[1] * tileheight + tileheight // 2
            target_pos = pygame.math.Vector2(target_x, target_y)
    
            direction = (target_pos - self.pos)
            
            if direction.length() > 0:
                direction = direction.normalize()
                next_pos = self.pos + direction * self.speed
                self.rect.center = (int(self.pos.x), int(self.pos.y))

                test_rect = self.rect.copy()
                test_rect.center = next_pos
                # Collision with walls
                collided = False
                for wall in wall_rect:
                    if test_rect.colliderect(wall):
                        collided = True
                        break
                    
                if not collided:
                    self.pos = next_pos
                else:
                    directions = [
                        (0, -1),  # Up
                        (0, 1),   # Down
                        (-1, 0),  # Left
                        (1, 0)    # Right
                    ]
                    moved = False
                    for dx, dy in directions:
                        test_pos = pygame.math.Vector2(self.pos.x + dx * self.speed, self.pos.y + dy * self.speed)
                        test_rect.center = test_pos
                        if not any(test_rect.colliderect(wall) for wall in wall_rect):
                            self.pos = test_pos
                            moved = True
                            break
                    if not moved:
                        # Optionally, recalculate the path again or wait
                        pass



        self.rect.center = self.pos
        self.turn_towards_player(player)
        distance = (player.pos - self.pos).length()
        if distance < settings.NORMAL_ENEMY_RANGE:
            self.shoot_at_player(player, bullet_group, camera_group)
    
        if self.shoot_cooldown > 0 :
            self.shoot_cooldown -= 1

        # You can add more AI logic here (e.g., attack, patrol, flee)

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()
    
