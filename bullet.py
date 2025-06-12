import pygame
import math
import settings
import math



class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, angle):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load(settings.BULLET_IMAGE).convert_alpha(), 0, settings.BULLET_SIZE)
        # pygame.draw.rect(self.image, (255, 255, 0), self.image.get_rect())
        self.image = pygame.transform.rotate(self.image, -angle)

        self.rect = self.image.get_rect(center=pos)


        # Convert angle to radians for velocity calculation
        rad = math.radians(angle)
        self.velocity = pygame.math.Vector2(math.cos(rad), math.sin(rad)) * settings.BULLET_SPEED

        self.initial_pos = pygame.Vector2(self.rect.center)
        
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

