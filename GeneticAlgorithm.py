import numpy as np
import pygame
import csv
from copy import deepcopy
from Bird import Bird

class GeneticAlgorithm:
    def __init__(self, population_size = 25, fitness_type = "complex", crossover_type = "fixed"):
        self.bird_img = pygame.image.load('Images/redbird-upflap.png')

        self.alive_birds = []
        self.dead_birds = []

        self.pop_size = population_size
        self.best_bird = Bird(self.bird_img)

        self.gen_num = -1        
        self.prev_gens_score = {} 
        
        self.fitness_type = fitness_type
        self.crossover_type = crossover_type

        self.initialize_population()

    def initialize_population(self):
        for i in range(self.pop_size):
            self.alive_birds.append(Bird(self.bird_img))

    def is_gen_dead(self):
        return len(self.alive_birds) == 0

    def get_next_generation(self):
        # Calculating fitness based on type
        if self.fitness_type == "simple":
            self.calc_fitness_simple()
        elif self.fitness_type == "complex":
            self.calc_fitness_complex()
            for i in range(25):
                # Add top 5 to next generation 
                if i < 5:
                    self.alive_birds.append(self.dead_birds[i])
                # Add 25 of the best bird to next generation
                self.alive_birds.append(Bird(self.bird_img, self.best_bird.nn))

        # Creating new population based on crossover
        if self.crossover_type == "none":
            for i in range(self.pop_size - len(self.alive_birds)):
                self.alive_birds.append(self.no_crossover()) 
        elif self.crossover_type == "fixed":  
            for i in range(self.pop_size - len(self.alive_birds)):
                self.alive_birds.append(self.crossover_fp())   
        elif self.crossover_type == "variable":  
            for i in range(self.pop_size - len(self.alive_birds)):
                self.alive_birds.append(self.crossover_vp())           

        self.dead_birds = [] 
        self.gen_num += 1
        
    # Calculates and normalizes the fitness score of birds using the time alive
    def calc_fitness_simple(self):
        total_fitness = 0

        for bird in self.dead_birds:
            bird.fitness = bird.time_alive
            total_fitness += bird.fitness
            if bird.score > self.best_bird.score:  
                self.best_bird = bird  

        # Normalize bird fitness values
        for bird in self.dead_birds:
            bird.fitness /= total_fitness 

    # Calculates and normalizes the fitness score of birds using the time alive + center dist.
    def calc_fitness_complex(self):
        total_fitness = 0

        for bird in self.dead_birds:
            bird.fitness = bird.time_alive - bird.center_dist
            total_fitness += bird.fitness
            if bird.score > self.best_bird.score:  
                self.best_bird = bird  

        # Normalize bird fitness values
        for bird in self.dead_birds:
            bird.fitness /= total_fitness 
        
        # Sort from high to low
        self.dead_birds.sort(key=lambda x: x.fitness, reverse=True)

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

    # No crossover used, basic selection and then mutation 
    def no_crossover(self):
        child = self.get_parent()
        child.mutate()
        return child

    # Fixed-point crossover (at halfway point)
    def crossover_fp(self):
        p1 = self.get_parent()
        p2 = self.get_parent()
        dims = p1.nn.shape()

        # First half of parent2 is assigned to parent1.
        p1.nn.weights['input'][dims[0]//2:dims[0]] = deepcopy(p2.nn.weights['input'][dims[0]//2:dims[0]])
        p1.nn.weights['hidden'][dims[1]//2:dims[1]] = deepcopy(p2.nn.weights['hidden'][dims[1]//2:dims[1]])
        # Merging biases from both parents to create child biases
        p1.nn.biases['input'][dims[0]//2:dims[0]] = deepcopy(p2.nn.biases['input'][dims[0]//2:dims[0]])
        p1.nn.biases['hidden'][dims[1]//2:dims[1]] = deepcopy(p2.nn.biases['hidden'][dims[1]//2:dims[1]])   

        child = p1
        child.mutate()
        return child

    # Variable-point crossover
    def crossover_vp(self):
        # Choosing parents and initializing dimensions
        p1 = self.get_parent()
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