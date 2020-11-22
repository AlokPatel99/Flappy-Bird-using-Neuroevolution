import pygame
import random

class Pipe:
    def __init__(self):
        self.colour = (211, 253, 117)

        self.width = 52
        self.height = random.randint(50,300)
        self.gap = 100
        
        self.x = 288
        self.dx = -1 

        self.score_sound = pygame.mixer.Sound('Sounds/sfx_point.wav')
    
    def display(self, screen):
        # Upper pipe
        pygame.draw.rect(screen, self.colour, (self.x, 0, self.width, self.height))
        # Lower pipe
        lower_pipe_height = 300 - self.height
        pygame.draw.rect(screen, self.colour, (self.x, self.height + self.gap, self.width, lower_pipe_height))
    
    def update(self, bird, dt):
        self.x += self.dx * dt
        
        if self.x <= -10:
            self.x = 288
            self.height = random.randint(50,300)

            if bird.dy != 0:
                pygame.mixer.Sound.play(self.score_sound)            
                return 1 
        return 0 

        

