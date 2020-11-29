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
                self.alive_birds.append(self.crossover_1())   #Changed as crossover added.(1 or 2 any)

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
        
       parent = Bird(self.bird_img, neural_network = bird.nn)
        return parent

    def gen_dead(self):
        return not len(self.alive_birds) > 0

    #Below Function returns the child after the crossover(50%) and the mutation.
    def crossover_1(self):
        parent1 = self.get_bird()
        parent2 = self.get_bird()
        w_input_p1 = parent1.nn.weights['input']
        w_input_p2 = parent2.nn.weights['input']
        w_hidden_p1 = parent1.nn.weights['hidden']
        w_hidden_p2 = parent2.nn.weights['hidden']
        '''
        print('ip_p1')
        print(w_input_p1)
        #print(w_input_p1[0:2])
        print('ip_p2')
        print(w_input_p2)
        #print(w_input_p2[2:4])
        print('h_p1')
        print(w_hidden_p1)
        print('h_p2')
        print(w_hidden_p2)
        '''
        # Making crossover, lower half of parent2 is assigned to parent1.
        w_input_p1[int(parent1.nn.input_nodes/2):int(parent1.nn.input_nodes)] = w_input_p2[int(parent2.nn.input_nodes/2):int(parent2.nn.input_nodes)]
        w_hidden_p1[int(parent1.nn.hidden_nodes/2):int(parent1.nn.hidden_nodes)] = w_hidden_p2[int(parent2.nn.hidden_nodes/2):int(parent2.nn.hidden_nodes)]
        '''
        print('updated_p1_ip')
        print(w_input_p1)
        print('updated_p1_h')
        print(w_hidden_p1)
        '''
        parent1.mutate()       #Mutation of the crossover.
        child = parent1
        return child
    
    # Crossover of 75 to 25 %, where the parent-1 retains its 75% data and 25% 
    # of the parent-2. So, 25% number of rows are replaced, in our case it is 
    # last row if input, and last two rows of the hidden.
    def crossover_2(self):
        parent1 = self.get_bird()
        parent2 = self.get_bird()
        w_input_p1 = parent1.nn.weights['input']
        w_input_p2 = parent2.nn.weights['input']
        w_hidden_p1 = parent1.nn.weights['hidden']
        w_hidden_p2 = parent2.nn.weights['hidden']
        '''
        print('ip_p1')
        print(w_input_p1)
        #print(w_input_p1[0:2])
        print('ip_p2')
        print(w_input_p2)
        #print(w_input_p2[2:4])
        print('h_p1')
        print(w_hidden_p1)
        print('h_p2')
        print(w_hidden_p2)
        '''
        w_input_p1[int(0.75*parent1.nn.input_nodes):int(parent1.nn.input_nodes)] = w_input_p2[int(0.75*parent2.nn.input_nodes):int(parent2.nn.input_nodes)]
        w_hidden_p1[int(0.75*parent1.nn.hidden_nodes):int(parent1.nn.hidden_nodes)] = w_hidden_p2[int(0.75*parent2.nn.hidden_nodes):int(parent2.nn.hidden_nodes)]
        '''
        print('updated_p1_ip')
        print(w_input_p1)
        print('updated_p1_h')
        print(w_hidden_p1)
        '''
        parent1.mutate()       #Mutation of the crossover.
        child = parent1
        return child
        
        

    
        
        
            
            
        
        
            
    
