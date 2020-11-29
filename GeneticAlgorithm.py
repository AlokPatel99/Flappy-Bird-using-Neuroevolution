import numpy as np
import pygame
from Bird import Bird

class GeneticAlgorithm:
    def __init__(self, population_size = 25):
        self.bird_img = pygame.image.load('Images/redbird-upflap.png')

        self.alive_birds = []
        self.dead_birds = []

        self.pop_size = population_size
        self.best_bird = Bird(self.bird_img)

        self.gen_num = -1        
        self.prev_gens_score = {} 

        self.initialize_population()

    def initialize_population(self):
        for i in range(self.pop_size):
            self.alive_birds.append(Bird(self.bird_img))

    def is_gen_dead(self):
        return len(self.alive_birds) == 0

    def get_next_generation(self):
        self.calculate_fitness()

        for i in range(self.pop_size):
            self.alive_birds.append(self.crossover_1())   

        self.dead_birds = [] 
        self.gen_num += 1
        
    # Calculates and normalizes the fitness score of birds
    def calculate_fitness(self):
        total_fitness = 0

        for bird in self.dead_birds:
            bird.fitness = bird.time_alive
            total_fitness += bird.fitness
            if bird.score > self.best_bird.score:  
                self.best_bird = bird  

        # Normalize bird fitness values
        for bird in self.dead_birds:
            bird.fitness /= total_fitness 

    # Choosing a bird through a probability weighted by higher fitness
    def get_bird(self):
        idx = 0
        r = np.random.uniform()
        while r > 0:
            r = r - self.dead_birds[idx].fitness
            idx += 1
        bird = self.dead_birds[idx-1]
        
        parent = Bird(self.bird_img, neural_network = bird.nn)
        return parent

    #Below Function returns the child after the crossover(50%) and the mutation.
    def crossover_1(self):
        parent1 = self.get_bird()
        p1_dims = parent1.nn.shape()

        parent2 = self.get_bird()
        p2_dims = parent2.nn.shape()

        w_input_p1 = parent1.nn.weights['input']
        w_input_p2 = parent2.nn.weights['input']
        w_hidden_p1 = parent1.nn.weights['hidden']
        w_hidden_p2 = parent2.nn.weights['hidden']

        # First half of parent2 is assigned to parent1.
        w_input_p1[p1_dims[0]//2:p1_dims[0]] = w_input_p2[p2_dims[0]//2:p2_dims[0]]
        w_hidden_p1[p1_dims[1]//2:p1_dims[1]] = w_hidden_p2[p2_dims[1]//2:p2_dims[1]]

        parent1.mutate() 
        child = parent1
        return child
    
    # Crossover of 75 to 25 %, where parent 1 retains 75% of its genes
    def crossover_2(self):
        parent1 = self.get_bird()
        p1_dims = parent1.nn.shape()

        parent2 = self.get_bird()
        p2_dims = parent2.nn.shape()

        w_input_p1 = parent1.nn.weights['input']
        w_input_p2 = parent2.nn.weights['input']
        w_hidden_p1 = parent1.nn.weights['hidden']
        w_hidden_p2 = parent2.nn.weights['hidden']

        # Lower quarter of parent2 is assigned to parent1.
        w_input_p1[p1_dims[0]//4:p1_dims[0]] = w_input_p2[p2_dims[0]//4:p2_dims[0]]
        w_hidden_p1[p1_dims[1]//4:p1_dims[1]] = w_hidden_p2[p2_dims[1]//4:p2_dims[1]]

        parent1.mutate() 
        child = parent1
        return child