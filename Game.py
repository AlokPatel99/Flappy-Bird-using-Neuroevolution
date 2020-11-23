# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 21:19:09 2020
AI Project
@authors: Rahul Behal and Alok Patel
""" 

# Imports
import pygame
import random
import sys
import time 
import json   
from Pipe import Pipe
from Bird import Bird
from NeuralNetwork import NeuralNetwork
from GeneticAlgorithm import GeneticAlgorithm

# Initialising the modules in pygame
pygame.init()
clock = pygame.time.Clock()

# Initializing display and associated parameters
screen = pygame.display.set_mode((288, 512))  
pygame.display.set_caption('Flappy Bird')
fps = 30
frame_skip = 5

# Loading sounds
collision_sound = pygame.mixer.Sound('Sounds/sfx_hit.wav')
 
# Initializing background
backgrounds = ('Images/background-day.png', 'Images/background-night.png')
background = pygame.image.load(random.choice(backgrounds))  
base = pygame.image.load('Images/base.png')

# Initializing main objects
pipe = Pipe()
bird = Bird()
NN = NeuralNetwork(5,1,1)

# Initialize score 
score = 0
score_font = pygame.font.SysFont('comicsansms',28, bold = True) 
 
# Initialization of GA
totalPopulation = 500
activeBirds = []
allBirds = []
pipes = []
counter = 0
highScore = 0
runBest = False
'''
# Created the population
for i in range(totalPopulation):
    bird_p = Bird()
    activeBirds[i] = bird_p
    allBirds[i] = bird_p
'''
# Main function that calls the NN and get the output of it.
# Returns True if need to jump.
def predict_action(x1, x2, x3, x4, x5):
    x = [ x1,x2,x3,x4,x5]
    Output = NN.predict(x)
    print(Output)
    if Output > 0.5:
        return True
    else:
        return False

game_over = False
while not game_over:

    # Display background
    screen.fill((0,0,0))
    screen.blit(background, (0,0))
    screen.blit(base, (0,400))
    
    # Keybindings
    for event in pygame.event.get():
        # If exit is pressed the game will quit.
        if event.type == pygame.QUIT:            
            running = False
        '''
        if event.type == pygame.KEYDOWN:
            # Move up on space bar
            if event.key == pygame.K_SPACE:
                bird.dy = -2 
        
        if event.type == pygame.KEYUP:
            # Re-enable gravity after space bar is lifted
            if event.key == pygame.K_SPACE:
                bird.dy = 1       
        '''
        action = predict_action(bird.y, pipe.height, pipe.height+pipe.gap, pipe.x, pipe.dx)
        
        if action:
            bird.dy = -2
        else:
            bird.dy = 1
            
        
    # Updating game
    dt = clock.tick(fps) / frame_skip
    score += pipe.update(bird, dt)
    game_over = bird.update(pipe, dt)
    
    # Display
    pipe.display(screen)
    bird.display(screen)

    score_display = score_font.render("Score: " + str(score), True, (0,0,0))
    screen.blit(score_display, (10,10))

    pygame.display.update()

    if game_over:
        pygame.mixer.Sound.play(collision_sound)
        time.sleep(1)
        pygame.quit()

    
#Quit the game, sys is used when game run on the Linux.
pygame.quit()
sys.exit()
