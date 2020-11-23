'''
Just the functions are defined from the refrence of the Coding Train work,
Need heavy changes inorder for the proper work.
'''

import numpy as np
import random

class GeneticAlgorithm:
    def __init__(self, ):
        
        
        
     def resetGame(self):
        self.counter = 0
        if self.bestBird:
            self.bestBird.score = 0
        
        self.pipes = []
        
    def nextGeneration(self):
        self.resetGame()
        self.normalizeFitness(self.allBirds)
        self.allBirds = self.activeBirds
        
    def generate(self,oldBirds):
        self.newBirds = []
        for i in range(len(self.oldBirds)):
            self.bird = self.poolSelection(self.oldBords)
            self.newBirds[i] = self.bird
        return self.newBirds

    def normalizeFitness(self,birds):
        for i in range(len(self.birds)):
            self.birds[i].score = pow(self.birds[i].score, 2)
        
        sum = 0 
        for i in range(len(self.birds)):
            sum += birds[i].score
            
        for i in range(len(self.birds)):
            self.birds[i].fitness = self.birds[i].score/sum
            
    def poolSelection(self,birds):
        self.index = 0
        r = random.uniform(0,1)
        while r>0:
            r -= self.birds[self.index].fitness
            self.index += 1 
        
        self.index -= 1
        return self.birds[self.index].copy()
        
    
        
        
            
            
        
        
            
    