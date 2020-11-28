# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 21:19:09 2020
AI Project
@authors: Rahul Behal and Alok Patel
""" 

# Imports
import pygame
import numpy as np
import sys
import time 
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
background = pygame.image.load(np.random.choice(backgrounds))  
base = pygame.image.load('Images/base.png')

# Initializing main objects
pipe = Pipe()
ga = GeneticAlgorithm(250)  #Changed the population from 50 to 250. 

# Initialize score and others
gen = -1
score = 0
font = pygame.font.SysFont('comicsansms',28, bold = True) 

# Below will solve the problem of the generation instant increase of 2 to 3 value.
def generate_or_not(pipe):
    if pipe.x < 70:              #30 is start of the bird, and end of bird is at 64.
        return False            #So if pipe is within 70, then new gen will not occur.
    else:
        return True

game_over = False
while not game_over:
    # Check for generation change
    if ga.gen_dead():
        # Below will solve the problem of the generation instant increase of 2 to 3 value.
        if gen > 0:     #This for other generations.
            if generate_or_not(pipe):
                ga.get_next_generation()
                gen = gen + 1
                score = 0
        else:           #This is just for the initialization.
             ga.get_next_generation()
             gen = gen + 1
             score = 0

    # Display background
    screen.fill((0,0,0))
    screen.blit(background, (0,0))
    screen.blit(base, (0,400))
    '''
    # Keybindings
    for event in pygame.event.get():
        # If exit is pressed the game will quit.
        if event.type == pygame.QUIT:            
            running = False
        
        if event.type == pygame.KEYDOWN:
            # Move up on space bar
            if event.key == pygame.K_SPACE:
                bird.jump() 
    '''
    # Choose action
    for bird in ga.alive_birds:
        if bird.predict_action(pipe):
            bird.jump()

    # Updating game
    dt = clock.tick(fps) / frame_skip
    score += pipe.update(dt)

    # Update birds
    dead_birds = []
    for bird in ga.alive_birds:
        is_dead = bird.update(pipe, dt)
        if is_dead:
            bird.score = score
            dead_birds.append(bird)
          
    # Update dead and alive bird arrays
    for bird in dead_birds:
        ga.alive_birds.remove(bird)
        ga.dead_birds.append(bird)
    
    # Display
    pipe.display(screen)
    for bird in ga.alive_birds:
        bird.display(screen)

    score_display = font.render("Score: " + str(score), True, (0,0,0))
    gen_display = font.render("Generation: " + str(gen), True, (0,0,0))     #ga.gen_num is replaced with gen.
    screen.blit(score_display, (10,10))
    screen.blit(gen_display, (10,40))

    pygame.display.update()
    if game_over:
        # pygame.mixer.Sound.play(collision_sound)
        # time.sleep(1)
        # pygame.quit()
        game_over = False

    
#Quit the game, sys is used when game run on the Linux.
pygame.quit()
sys.exit()
