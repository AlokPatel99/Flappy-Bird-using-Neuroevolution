import pygame
from NeuralNetwork import *

class Bird:
    def __init__(self, img, neural_network=None):
        # Display parameters
        self.img = img
        self.width = self.img.get_width()
        self.height = self.img.get_height()

        # Position and derivative parameters
        self.x = 30
        self.y = 300
        
        self.velocity = 0
        self.gravity = 0.225

        # Neuroevolution parameters
        self.score = 0
        self.fitness = 0
        self.time_alive = 0

        if neural_network is not None:
            self.nn = neural_network.copy()
        else:
            self.nn = NeuralNetwork(4,8,1)          

    def display(self, screen):
        screen.blit(self.img, (self.x, self.y))

    def jump(self):
        if self.velocity >= 0:    
            self.velocity = -2
    
    # Updates position parameters and derivatives
    # Returns True if bird died, False if alive
    def update(self, pipe, dt):
        self.time_alive += 1  
        
        self.velocity += self.gravity
        self.y += self.velocity * dt

        if self.y <= 0:
            self.y = 0
        elif self.y >= 380:
            # Game over if bird falls to ground
            self.y = 380 
            return True
        
        return self.is_collision(pipe)

    def is_collision(self, pipe):
        if pipe.x <= self.x + self.width and pipe.x + pipe.width >= self.x:
            lower_pipe_height = pipe.height + pipe.gap 
            if self.y <= pipe.height or self.y >= lower_pipe_height - self.height:
                return True
        return False

    def mutate(self, rate = 0.1):
        self.nn.mutate(rate)

    # Main function that calls the NN and get the output of it. 
    # Returns True if need to jump.
    def predict_action(self, pipe):
        inputs = []
        # Inputs divided by max value to normalize
        inputs.append(self.y / 400)
        inputs.append(pipe.height / 400)
        inputs.append(np.maximum(0, pipe.x / 300))
        inputs.append(self.velocity / 4)

        output = self.nn.predict(inputs)
        if output > 0.5:
            return True
        else:
            return False




        

