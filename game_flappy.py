# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 21:19:09 2020
AI Project
@authors: Rahul Behal and Alok Patel
""" 

import pygame
import random
import sys
import time    

# Initialising the modules in pygame
pygame.init()

#Setting the Screen and window caption name 
Screen = pygame.display.set_mode((288, 512))    #Setting the display
pygame.display.set_caption('Flappy Bird')

#Load Sounds
Point_sound = pygame.mixer.Sound('Sounds/sfx_point.wav')
Hit_sound = pygame.mixer.Sound('Sounds/sfx_hit.wav')
 
#Background
Background_list = ('Images/background-day.png', 'Images/background-night.png')
randbg = random.randint(0, len(Background_list) - 1)
Background = pygame.image.load(Background_list[randbg])  #Background selected randomly

#Base
Base = pygame.image.load('Images/base.png')

#Pipes, and two pipes at one time in the screen.
Pipe_lower = pygame.image.load('Images/pipe-green.png')
Pipe_upper = pygame.image.load('Images/pipe-green-inverted.png')
pipe_height = random.randint(80,300)        #Height for the top obstacle for 1st iter. Used for rectangle.
pipe_width = 52    
pipe_width_all = [52, 52+80]    # 80 pixels is the distance set between the two pipes.
#Lower_pipe = [random.randrange(250, 380), random.randrange(250, 380)]   #Height of lower pipe.
#Upper_pipe = [random.randrange(-300, -170), random.randrange(-300, -170)]
# Below three specifications are used, when the rectangles are used.
pipe_x_change = -1              # Pipes move at this rate in negative x
pipe_x = 288                    # Ending of the screen
Pipe_color = (211, 253, 117)    # Removed when real pipes are addded.

#Bird
''' Similarly random bird color can be set '''
Bird = pygame.image.load('Images/redbird-upflap.png')
bird_x = 30         #Will remian fixed throughout the game. 
bird_y = 300        #Will wary according to the move.
bird_y_change = 0   #Initialized with 0, later changed by the flap.

# Displaying the bird.
def display_bird(x,y):
    Screen.blit(Bird, (x,y))

# Displaying the pipe on the screen. height is the random generated.
def display_pipe(height):
    #This three lines are just basic rectangle representation.

    pygame.draw.rect(Screen, Pipe_color, (pipe_x, 0, pipe_width, height))
    bottom_obstacle_height = 400 - height - 100
    pygame.draw.rect(Screen, Pipe_color, (pipe_x, 400, pipe_width, -bottom_obstacle_height))

    #pipe_height_bottom = 
    #For lower pipe   

# Checking the collider.
def collison_detection(pipe_x, pipe_height, bird_y, pipe_height_bottom):
    # 30 is the bird start and the 34 is bird width.
    if pipe_x >= 30 and pipe_x <= (30+34):
        # Bird collides the pipe than returns true. 24 is the height of the bird.
        if bird_y <= pipe_height or bird_y >= (pipe_height_bottom -24):
            return True
    return False

# Score Display
score = 0
Score_font = pygame.font.SysFont('comicsansms',28, bold = True) 
 
def score_display(score):
    display = Score_font.render("Score: " + str(score), True, (0,0,0))
    Screen.blit(display, (10,10))

running = True

while running:
    
    Screen.fill((0,0,0))
    #display the background image
    Screen.blit(Background, (0,0))
    Screen.blit(Base, (0,400))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #If exit is pressed the game will quit.
            running = False
        
        #Later for both if will be replaced with the AI function.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_y_change = -2     # When flap then move up by 2 
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                bird_y_change = 1       # When not done anything, goes down by 1
        
    # Vertical movement of the bird
    bird_y += bird_y_change
    
    # Y limit of the bird to go up and down.(Boundary)
    if bird_y <= 0:
        bird_y = 0
    if bird_y >= 380:
        bird_y = 380        #As at 380 the base is started so we stop.
    
    #Moving the pipe
    pipe_x += pipe_x_change
         
   #Creating the new Pipe. Also increasing the point.
    if pipe_x <= -10:  
        pipe_x = 288
        pipe_height = random.randint(50, 330)  #Used when basic triangles were placed.
        score += 1
        pygame.mixer.Sound.play(Point_sound)
        #Point_sound.play()
        
        # Lower Pipe can start from 250 to 380 pixel, this can be experiment with different values.
        #pipe_height_lower = random.randrange(250, 380)
        # Upper Pipe can start from -170 to -300 pixel
        #pipe_height_upper = random.randrange(-300, -170)
    
    #Collison detector. 100 is the gap length.
    collison = collison_detection(pipe_x, pipe_height, bird_y, pipe_height + 100)
     
    if collison:
        #Hit_sound.play()    
        pygame.mixer.Sound.play(Hit_sound)
        time.sleep(1)
        pygame.quit()
        
    #Display the Pipe.
    display_pipe(pipe_height)
    #display_pipe()
    
    #Display the bird.
    display_bird(bird_x, bird_y)
    
    #Display of the Score
    score_display(score)
    
    #Update the display after each iteration of the while loop.
    pygame.display.update()
    
#Quit the game, sys is used when game run on the Linux.
pygame.quit()
sys.exit()



