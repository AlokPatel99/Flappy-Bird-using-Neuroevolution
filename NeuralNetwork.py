import numpy as np
from copy import deepcopy

class NeuralNetwork:
    def __init__(self, input_nodes, hidden_nodes, output_nodes, weights = None, biases = None): 
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes 

        if weights is not None and biases is not None:
            self.weights = weights
            self.biases = biases
            return

        self.weights = {}
        self.biases = {}
        self.initialize_layers()

    def initialize_layers(self):
        # Input layer
        self.weights['input'] = np.random.randn(self.input_nodes, self.hidden_nodes)
        self.biases['input'] = np.random.randn(1, self.hidden_nodes)

        # Hidden layer
        self.weights['hidden'] = np.random.randn(self.hidden_nodes, self.output_nodes)
        self.biases['hidden'] = np.random.randn(1, self.output_nodes)        

    def predict(self, x):
        x1 = np.dot(x,self.weights['input']) + self.biases['input']
        x1 = self.relu(x1)

        x2 = x1.dot(self.weights['hidden']) + self.biases['hidden']
        y = self.sigmoid(x2)
        return y

    def relu(self, x):
        return np.maximum(0, x)

    def sigmoid(self, x):
        return 1/(1+np.exp(-x))

    def shape(self):
        return self.input_nodes, self.hidden_nodes, self.output_nodes
    
    def mutate(self, rate):
        # Mutates a single number -- Mapped to weight and bias arrays 
        def mutation(x, rate):
            if np.random.uniform() < rate:
                offset = np.random.uniform(-0.225,0.225);
                newx = x + offset
                return newx
            else:
                return x

        # Mutate input layer parameters - Maps mutation function to weight matrix and bias vector
        self.weights['input'] = np.vectorize(mutation)(self.weights['input'], rate=rate)
        self.biases['input'] = np.vectorize(mutation)(self.biases['input'], rate=rate)
        # Mutate hidden layer parameters - Maps mutation function to weight matrix and bias vector
        self.weights['hidden'] = np.vectorize(mutation)(self.weights['hidden'], rate=rate)
        self.biases['hidden'] = np.vectorize(mutation)(self.biases['hidden'], rate=rate)

    def copy(self):
        i = self.input_nodes
        h = self.hidden_nodes
        o = self.output_nodes

        weights = deepcopy(self.weights)
        biases = deepcopy(self.biases)
        
        return NeuralNetwork(i,h,o,weights,biases)