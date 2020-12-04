# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 21:19:09 2020
Flappy Bird Using Neuroevolution
@authors: Rahul Behal and Alok Patel
""" 

# Imports
import pygame
import numpy as np
import sys
import time 
import matplotlib.pyplot as plt
from Pipe import Pipe
from GeneticAlgorithm import GeneticAlgorithm

# Initialising the modules in pygame
pygame.init()
clock = pygame.time.Clock()

# Initializing display and associated parameters
screen = pygame.display.set_mode((288, 512))  
pygame.display.set_caption('Flappy Bird')
fps = 60
frame_skip = 5

# Loading sounds
collision_sound = pygame.mixer.Sound('Sounds/sfx_hit.wav')
 
# Initializing background
backgrounds = ('Images/background-day.png', 'Images/background-night.png')
background = pygame.image.load(np.random.choice(backgrounds))  
base = pygame.image.load('Images/base.png')

# Initializing training speed and buttons
training_speed = 1

btn_size = (30, 30)
btn_pos = (250, 450)
btn_gap = 40 

speed_up_btn = pygame.image.load('Images/speed-up.png')  
speed_up_btn = pygame.transform.scale(speed_up_btn, btn_size)

slow_down_btn = pygame.image.load('Images/slow-down.png')  
slow_down_btn = pygame.transform.scale(slow_down_btn, btn_size)

# Learning functions
fitness_type = "complex"
crossover_type = "variable"
activation_type = "tanh"

# Initializing main objects
pipe = Pipe()
ga = GeneticAlgorithm(
                      fitness_type=fitness_type,
                      crossover_type=crossover_type,
                      activation_type=activation_type
                     )  

# Initialize score and other
score = 0
font = pygame.font.SysFont('Helvetica',28, bold = True) 

game_over = False
while not game_over:
    # Update ticks and set change value
    dt = clock.tick(fps) / frame_skip

    # Check for user interaction with window
    (mouse_x, mouse_y) = pygame.mouse.get_pos()
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            pygame.quit() 
        if event.type == pygame.MOUSEBUTTONDOWN: 
            # Check if speed up button was pressed
            if btn_pos[0] <= mouse_x <= btn_pos[0]+btn_size[0] and btn_pos[1] <= mouse_y <= btn_pos[1]+btn_size[1]: 
                training_speed += 1
            # Check if slow down button was pressed
            elif btn_pos[0]-btn_gap <= mouse_x <= btn_pos[0]-btn_gap+btn_size[0] and btn_pos[1] <= mouse_y <= btn_pos[1]+btn_size[1]:
                if training_speed > 1:
                    training_speed -= 1
        if event.type == pygame.KEYDOWN:
            if pygame.key.name(event.key) == "s":
                ga.save_csv()
    
    for i in range(training_speed):
        # Check for generation change
        if ga.is_gen_dead():
            if pipe.x > 250 or ga.gen_num == -1:
                ga.get_next_generation()
                ga.prev_gens_score[ga.gen_num] = score
                print('Generation: {}\nScore: {}\n'.format(ga.gen_num, score))
                score = 0

        # Choose action
        for bird in ga.alive_birds:
            if bird.predict_action(pipe):
                bird.jump()

        # Updating game
        score += pipe.update(dt)

        # Update birds
        dead_birds = []
        for bird in ga.alive_birds:
            is_dead = bird.update(pipe, dt)
            if is_dead:
                bird.died(pipe, score)
                dead_birds.append(bird)
            
        # Update dead and alive bird arrays
        for bird in dead_birds:
            ga.alive_birds.remove(bird)
            ga.dead_birds.append(bird)
        
    # Display background
    screen.fill((0,0,0))
    screen.blit(background, (0,0))
    screen.blit(base, (0,400))

    # Display pipes and birds
    pipe.display(screen)
    for bird in ga.alive_birds:
        bird.display(screen)

    # Display score and generation # 
    score_display = font.render("Score: %d" % score, True, (0,0,0))
    gen_display = font.render("Generation: %d" % (ga.gen_num + 1), True, (0,0,0))
    screen.blit(score_display, (10,10))
    screen.blit(gen_display, (10,40))

    # Display training speed buttons
    screen.blit(speed_up_btn, btn_pos)
    screen.blit(slow_down_btn, (btn_pos[0] - btn_gap, btn_pos[1]))    

    pygame.display.update()
    if game_over:
        # pygame.mixer.Sound.play(collision_sound)
        # time.sleep(1)
        # pygame.quit()
        game_over = False
    
#Quit the game, sys is used when game run on the Linux.
pygame.quit()
sys.exit()
