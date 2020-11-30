import numpy as np
import pygame
import csv
from copy import deepcopy
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

    # Selecting a parent through a probability distribution weighted by fitness
    def get_parent(self):
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
        p1 = self.get_parent()
        p2 = self.get_parent()
        dims = p1.nn.shape()

        # First half of parent2 is assigned to parent1.
        p1.nn.weights['input'][dims[0]//2:dims[0]] = deepcopy(p2.nn.weights['input'][dims[0]//2:dims[0]])
        p1.nn.weights['hidden'][dims[1]//2:dims[1]] = deepcopy(p2.nn.weights['hidden'][dims[1]//2:dims[1]])

        child = p1
        child.mutate()
        return child

    # Single-point crossover
    def crossover_sp(self):
        # Choosing parents and initializing dimensions
        p1 = Bird(self.bird_img, neural_network = self.best_bird.nn)
        p2 = self.get_parent()
        dims = p1.nn.shape()

        # Choosing a single point at random to swap genes
        input_swap_idx = np.random.randint(0, dims[0]+1)
        hidden_swap_idx = np.random.randint(0, dims[1]+1)

        # Merging weights from both parents to create child weights
        p1.nn.weights['input'][input_swap_idx:dims[0]] = deepcopy(p2.nn.weights['input'][input_swap_idx:dims[0]])
        p1.nn.weights['hidden'][hidden_swap_idx:dims[1]] = deepcopy(p2.nn.weights['hidden'][hidden_swap_idx:dims[1]])
        # Merging biases from both parents to create child biases
        p1.nn.biases['input'][input_swap_idx:dims[0]] = deepcopy(p2.nn.biases['input'][input_swap_idx:dims[0]])
        p1.nn.biases['hidden'][hidden_swap_idx:dims[1]] = deepcopy(p2.nn.biases['hidden'][hidden_swap_idx:dims[1]])        

        child = p1
        child.mutate() 
        return child

    # Writes csv file with training data (gen numbers and scores)
    def save_csv(self):
        with open("training_data" + ".csv", 'w', newline='') as csv_file:
            # Initialize headers for CSV file
            headings = ["Generation Number", "Highest Score"]
            headings = headings
            # Writing headers
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(headings)
            # Writing data
            for gen in self.prev_gens_score:
                data = [gen, self.prev_gens_score[gen]]
                writer.writerow(data)