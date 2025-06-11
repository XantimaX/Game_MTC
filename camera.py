import pygame
import settings

class Camera(pygame.sprite.Group):
    def __init__(self, zoom, player):
        super().__init__()
        self.offset = pygame.math.Vector2()
        self.zoom = zoom
        self.player = player
        self.camera_offset = pygame.Vector2()

        self.display_surface = pygame.display.get_surface()
        self.half_w = self.display_surface.get_width() // 2
        self.half_h = self.display_surface.get_height() // 2

    def draw(self, surface):
        self.camera_offset.x = self.player.rect.centerx - (settings.WIDTH / (2 * self.zoom))
        self.camera_offset.y = self.player.rect.centery - (settings.HEIGHT / (2 * self.zoom))

        #temp surface for zooming
        temp_surface = pygame.Surface(
            (int(surface.get_width() / self.zoom), int(surface.get_height() / self.zoom))
        ).convert_alpha()
        temp_surface.fill((0, 0, 0, 0))
        
        for sprite in self.sprites() :
            
            if sprite is not self.player :
                offset_pos = sprite.rect.topleft - self.camera_offset
                temp_surface.blit(sprite.image, offset_pos)
        
        player_offset_pos = self.player.rect.topleft - self.camera_offset
        temp_surface.blit(self.player.image, player_offset_pos)

        scaled_surface = pygame.transform.smoothscale(
            temp_surface, surface.get_size()
        )
        surface.blit(scaled_surface, (0, 0))