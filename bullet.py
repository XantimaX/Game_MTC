import pygame
import math

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, angle, speed=15):
        super().__init__()
        self.image = pygame.Surface((12, 4), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (255, 255, 0), self.image.get_rect())
        self.image = pygame.transform.rotate(self.image, -angle)
        self.rect = self.image.get_rect(center=pos)
        # Convert angle to radians for velocity calculation
        rad = math.radians(angle)
        self.velocity = pygame.math.Vector2(math.cos(rad), math.sin(rad)) * speed
        
    def update(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        # Remove if off screen
        screen_rect = pygame.display.get_surface().get_rect()
        if not screen_rect.colliderect(self.rect):
            self.kill()