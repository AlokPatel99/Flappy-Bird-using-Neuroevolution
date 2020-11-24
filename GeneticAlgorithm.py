import numpy as np
import pygame
from Bird import Bird

class GeneticAlgorithm:
    def __init__(self, population_size = 25):
        self.bird_img = pygame.image.load('Images/redbird-upflap.png')

        self.alive_birds = []
        self.dead_birds = []

        self.pop_size = population_size
        self.gen_num = 1        
        self.best_bird = None

        self.initialize_population()

    def initialize_population(self):
        for i in range(self.pop_size):
            self.alive_birds.append(Bird(self.bird_img))

    def get_next_generation(self):
        # TODO: Fix this so new generation is based on some type of crossover mechanism
        #       Also, see what to do if the entire generation scores 0 
        is_all_zero = self.calculate_fitness()
        if is_all_zero:
            self.initialize_population()
        else:
            for i in range(self.pop_size):
                self.alive_birds.append(self.get_bird())

        self.dead_birds = [] 
        self.gen_num += 1
        
    # Calculates and normalizes the fitness score of birds
    # Returns True if all the scores were 0, False otherwise
    # TODO: Figure out what to do if the entire generation scores 0.
    #       Currently essentially resets all progress if one gen. scores all 0.
    def calculate_fitness(self):
        # Calculate total score from all birds and get best bird
        total_score = 0
        best_score = 0

        for bird in self.dead_birds:
            #total_score += bird.score
            total_score += bird.highest_live    #New added
            #if bird.score > best_score:
            if bird.highest_live > best_score:  #New added
                self.best_bird = bird  

        if total_score == 0:
            return True
        # Normalize score and assign that as a fitness value
        for bird in self.dead_birds:
            bird.fitness = bird.highest_live / total_score  #New added
            #bird.fitness = bird.score / total_score
        return False

    # Choosing a bird through a probability weighted by higher fitness
    # TODO: Replace with some sort of crossover
    def get_bird(self):
        idx = 0
        r = np.random.uniform()
        while r > 0:
            r = r - self.dead_birds[idx].fitness
            idx += 1
        bird = self.dead_birds[idx-1]
        
        child = Bird(self.bird_img, neural_network = bird.nn)
        child.mutate()
        return child

    def gen_dead(self):
        return not len(self.alive_birds) > 0


    
        
        
            
            
        
        
            
    
