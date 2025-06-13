import pygame

class ElapsedTimer:
    def __init__(self):
        self.start_time = pygame.time.get_ticks()
        self.paused = False
        self.pause_time = 0

    def reset(self):
        self.start_time = pygame.time.get_ticks()
        self.paused = False
        self.pause_time = 0

    def get_elapsed(self):
        if self.paused:
            return (self.pause_time - self.start_time) // 1000  # in seconds
        else:
            return (pygame.time.get_ticks() - self.start_time) // 1000  # in seconds

    def pause(self):
        if not self.paused:
            self.paused = True
            self.pause_time = pygame.time.get_ticks()

    def resume(self):
        if self.paused:
            paused_duration = pygame.time.get_ticks() - self.pause_time
            self.start_time += paused_duration
            self.paused = False