import pygame
import random

class Bird:
    def __init__(self):
        self.img = pygame.image.load('Images/redbird-upflap.png')
        
        self.width = self.img.get_width()
        self.height = self.img.get_height()

        self.x = 30
        self.y = 300
        
        self.dy = 0

    def display(self, screen):
        screen.blit(self.img, (self.x, self.y))
    
    def update(self, pipe, dt):
        if self.dy == 0:
            return 0
        self.y += self.dy * dt

        if self.y <= 0:
            self.y = 0
        elif self.y >= 380:
            self.y = 380 
        
        return self.is_collision(pipe)

    def is_collision(self, pipe):
        if pipe.x <= self.x + self.width and pipe.x + pipe.width >= self.x:
            lower_pipe_height = pipe.height + pipe.gap 
            if self.y <= pipe.height or self.y >= lower_pipe_height - self.height:
                return True
        return False




        

