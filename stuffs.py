import pygame
import math
import settings
import math
import os

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, angle, owner):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load(settings.BULLET_IMAGE).convert_alpha(), 0, settings.BULLET_SIZE)
        # pygame.draw.rect(self.image, (255, 255, 0), self.image.get_rect())
        self.image = pygame.transform.rotate(self.image, -angle)

        self.rect = self.image.get_rect(center=pos)


        # Convert angle to radians for velocity calculation
        rad = math.radians(angle)
        self.velocity = pygame.math.Vector2(math.cos(rad), math.sin(rad)) * settings.BULLET_SPEED

        self.initial_pos = pygame.Vector2(self.rect.center)
        self.owner = owner

    def update(self, map_width, map_height, wall_rect):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        
        distance_travelled = self.initial_pos.distance_to(pygame.Vector2(self.rect.center))

        #if outside the range
        if (distance_travelled >= settings.BULLET_RANGE):
            self.kill()

        # Remove if off screen
        if (self.rect.right < 0 or self.rect.left > map_width or
            self.rect.bottom < 0 or self.rect.top > map_height):
            self.kill()

        #wall collision
        for wall in wall_rect:
            if self.rect.colliderect(wall):
                self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        """
        center: (x, y) tuple for explosion center
        scale: float, scale factor for explosion images
        frame_paths: list of file paths to explosion animation frames
        """
        super().__init__()
        self.images = []
        # Load and scale frames
        frame_paths = os.listdir(settings.EXPLOSION_IMAGE_PATH)
        scale = settings.EXPLOSION_SCALE
        if frame_paths is not None:
            for path in frame_paths:
                img = pygame.image.load(os.path.join("Assets", "explosion", path)).convert_alpha()
                if scale != 1.0:
                    img = pygame.transform.scale(
                        img,
                        (int(img.get_width() * scale), int(img.get_height() * scale))
                    )
                self.images.append(img)
        else:
            # Fallback: load default frames if provided elsewhere
            raise ValueError("No explosion frame paths provided.")

        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.counter = 0
        self.frame_speed = 4  # Higher = slower animation

    def update(self):
        self.counter += 1
        if self.counter >= self.frame_speed:
            self.counter = 0
            self.frame_index += 1
            if self.frame_index >= len(self.images):
                self.kill()
            else:
                # Maintain center position
                center = self.rect.center
                self.image = self.images[self.frame_index]
                self.rect = self.image.get_rect()
                self.rect.center = center


class Grenade(pygame.sprite.Sprite):
    def __init__(self, pos, target_pos, grenade_image, speed,  explosion_damage, player):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load(grenade_image).convert_alpha(), 0, settings.GRENADE_SIZE)
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(pos)
        direction = (pygame.math.Vector2(target_pos) - self.pos)
        if direction.length() > 0:
            direction = direction.normalize()
        self.velocity = direction * speed
        self.timer = settings.GRENADE_FUSE  # frames or milliseconds
        self.explosion_damage = explosion_damage
        self.player = player

    def update(self, player, explosion_group, camera_group):
        # Move grenade
        self.pos += self.velocity
        self.rect.center = self.pos

        # Countdown timer
        # self.timer -= 1
        if self.rect.colliderect(player):
            self.explode(explosion_group, camera_group)
            self.player.take_damage(settings.GRENADE_DAMAGE)

    def explode(self,explosion_group, camera_group):
        # Create explosion sprite (optional visual)
        explosion = Explosion(self.pos)
        explosion_group.add(explosion)
        camera_group.add(explosion)

        self.kill()

                

