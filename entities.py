import pygame
import json
import settings
import math
from stuffs import Bullet, Grenade
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
        
        self.lives = 3

        self.health = settings.PLAYER_HEALTH
        self.spawn_point = (settings.PLAYER_START_X, settings.PLAYER_START_Y)

        self.damage_overlay_alpha = 0
        self.damage_overlay_max_alpha = 120  # Adjust for how       "red" you want
        self.damage_overlay_fade_rate = 10   # How fast the red         fades
        self.took_damage = False

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

    def draw_health_bar(self, surface, x, y, width, height):
        ratio = max(self.health / settings.PLAYER_HEALTH, 0)
        # Draw background (max health)
        pygame.draw.rect(surface, (60, 0, 0), (x, y, width, height))
        # Draw foreground (current health)
        pygame.draw.rect(surface, (0, 200, 0), (x, y, int(width * ratio),   height))
        # Optional: draw border
        pygame.draw.rect(surface, (255, 255, 255), (x, y, width, height), 2)
    
    def draw_lives_counter(self,surface, x, y, font=None):
        if font is None:
            font = pygame.font.SysFont(None, 32)
        lives_text = font.render(f"Lives: {self.lives}",     True,   (255, 255, 255))
        surface.blit(lives_text, (x, y))
        
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
            self.bullet = Bullet(pos = self.pos, angle = self.angle, owner = "player")
            bullet_group.add(self.bullet)
            camera_group.add(self.bullet)

    def check_bullet_collision(self, bullet_group):
        for bullet in pygame.sprite.spritecollide(self, bullet_group, False):
            if bullet.owner == "enemy":
                self.take_damage(settings.BULLET_DAMAGE)
                bullet.kill()
    
    def respawn(self) :
        self.health = settings.PLAYER_HEALTH
        self.pos = pygame.math.Vector2(self.spawn_point)
        self.rect.center = self.pos

    def game_over(self):
        print("Game Over")
    
    def take_damage(self,damage):
        self.health -= damage

        self.damage_overlay_alpha = self.damage_overlay_max_alpha  # Trigger red flash
        self.took_damage = True
        if self.health <= 0:
            self.lives -= 1
            if self.lives > 0:
                self.respawn()
            else:
                self.game_over()
        
        print(f"current health : {self.health}")

    def update(self, wall_rect, bullet_group, camera_group):
        
        self.user_input(bullet_group=bullet_group, camera_group = camera_group, )
        self.move(wall_rect = wall_rect)
        
        if self.damage_overlay_alpha > 0:
            self.damage_overlay_alpha = max(0, self.damage_overlay_alpha - self.damage_overlay_fade_rate)
        
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
        
        self.check_bullet_collision(bullet_group=bullet_group)
        
        self.player_turning()


class NormalEnemy(pygame.sprite.Sprite):
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
        self.health =  self.max_health = settings.NORMAL_ENEMY_HEALTH
        self.shoot_cooldown = 0
        self.pathfind_cooldown = settings.PATHFIND_COOLDOWN
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
    
    def check_bullet_collision(self, bullet_group):
        for bullet in pygame.sprite.spritecollide(self, bullet_group, False):
            if bullet.owner == "player":
                self.take_damage(settings.BULLET_DAMAGE)
                bullet.kill()
    
    def shoot_at_player(self, player, bullet_group, camera_group):
        if self.shoot_cooldown == 0:
            # Calculate angle to player
            dx = player.pos.x - self.pos.x
            dy = player.pos.y - self.pos.y
            angle = math.degrees(math.atan2(dy, dx))
            # Create and add bullet
            bullet = Bullet(pos=self.pos, angle=angle, owner = "enemy")
            bullet_group.add(bullet)
            camera_group.add(bullet)
            # Set cooldown (e.g., 30 frames for half a second at 60 fps)
            self.shoot_cooldown = settings.ENEMY_SHOOT_COOLDOWN
        
    def update(self, player, wall_rect, bullet_group, camera_group, grid, tmx_data):
        # Simple AI: move toward player
        
        tilewidth,tileheight = tmx_data.tilewidth, tmx_data.tileheight
        enemy_grid = world_to_grid(pos = self.pos, tileheight= tileheight, tilewidth=tilewidth)
        player_grid = world_to_grid(pos = player.pos, tileheight= tileheight, tilewidth=tilewidth)
        
        self.check_bullet_collision(bullet_group=bullet_group)

        if enemy_grid != self.last_grid_pos or player_grid != self.last_player_grid_pos or not self.path:
            self.path = astar(grid, enemy_grid, player_grid)
            self.last_grid_pos = enemy_grid
            self.last_player_grid_pos = player_grid

        
        direction = pygame.math.Vector2(player.pos) - self.pos

        if self.pathfind_cooldown == 0 and self.path and len(self.path) > 1:
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
                



        self.rect.center = self.pos
        self.turn_towards_player(player)
        distance = (player.pos - self.pos).length()
        if distance < settings.NORMAL_ENEMY_RANGE:
            self.shoot_at_player(player, bullet_group, camera_group)
    
        if self.shoot_cooldown > 0 :
            self.shoot_cooldown -= 1
        if self.pathfind_cooldown > 0 :
            self.pathfind_cooldown -= 1
        # You can add more AI logic here (e.g., attack, patrol, flee)

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()

class BruteEnemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.transform.rotozoom(
            pygame.image.load(settings.BRUTE_ENEMY_IMAGE).convert_alpha(), 0, settings.BRUTE_ENEMY_SIZE
        )

        self.base_sprite = self.image

        self.pos = pygame.math.Vector2(pos)
        self.hitbox_rect = self.base_sprite.get_rect(center = self.pos)
        self.rect = self.hitbox_rect.copy()

        self.speed = settings.BRUTE_ENEMY_SPEED
        self.health =  self.max_health = settings.NORMAL_ENEMY_HEALTH
        self.shoot_cooldown = 0
        self.pathfind_cooldown = settings.PATHFIND_COOLDOWN
        #path finding shenanigans
        self.path = []
        self.last_grid_pos = None
        self.last_player_grid_pos = None
        self.out_of_range_timer = 0
        self.grenade_cooldown = 0

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
            bullet = Bullet(pos=self.pos, angle=angle, owner = "enemy")
            bullet_group.add(bullet)
            camera_group.add(bullet)
            # Set cooldown (e.g., 30 frames for half a second at 60 fps)
            self.shoot_cooldown = settings.ENEMY_SHOOT_COOLDOWN
    

    def throw_grenade(self, player, grenade_group, camera_group):
        grenade = Grenade(
            pos=self.pos,
            target_pos=player.pos,
            grenade_image=settings.GRENADE_IMAGE,
            speed=settings.GRENADE_SPEED,
            explosion_damage=settings.GRENADE_DAMAGE,
            player = player
        )
        grenade_group.add(grenade)
        camera_group.add(grenade)

    def update(self, player, wall_rect, bullet_group, camera_group, grenade_group, grid, tmx_data):
        # Simple AI: move toward player
        
        tilewidth,tileheight = tmx_data.tilewidth, tmx_data.tileheight
        enemy_grid = world_to_grid(pos = self.pos, tileheight= tileheight, tilewidth=tilewidth)
        player_grid = world_to_grid(pos = player.pos, tileheight= tileheight, tilewidth=tilewidth)
        
        if enemy_grid != self.last_grid_pos or player_grid != self.last_player_grid_pos or not self.path:
            self.path = astar(grid, enemy_grid, player_grid)
            self.last_grid_pos = enemy_grid
            self.last_player_grid_pos = player_grid

        self.check_bullet_collision(bullet_group=bullet_group)
        
        direction = pygame.math.Vector2(player.pos) - self.pos

        if self.pathfind_cooldown == 0 and self.path and len(self.path) > 1:
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

        self.rect.center = self.pos
        self.turn_towards_player(player)
        distance = (player.pos - self.pos).length()
        if distance < settings.BRUTE_ENEMY_RANGE:
            self.shoot_at_player(player, bullet_group, camera_group)

        if self.shoot_cooldown > 0 :
            self.shoot_cooldown -= 1
        if self.pathfind_cooldown > 0 :
            self.pathfind_cooldown -= 1
        
        if distance > settings.GRENADE_RANGE_MIN :
            self.out_of_range_timer += 1
            if self.out_of_range_timer > settings.BRUTE_OUT_OF_RANGE_TIMER and self.grenade_cooldown == 0:
                self.throw_grenade(player, grenade_group, camera_group)
                self.grenade_cooldown = settings.GRENADE_COOLDOWN
                self.out_of_range_timer = 0
        else:
            self.out_of_range_timer = 0

        if self.grenade_cooldown > 0:
            self.grenade_cooldown -= 1
                # You can add more AI logic here (e.g.,     attack,     patrol, flee)
    def check_bullet_collision(self, bullet_group):
        for bullet in pygame.sprite.spritecollide(self, bullet_group, False):
            if bullet.owner == "player":
                self.take_damage(settings.BULLET_DAMAGE)
                bullet.kill()
    
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()


