import numpy as np

class NeuralNetwork:
    def __init__(self, input_nodes, hidden_nodes, output_nodes):
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes 

        self.weights = {}
        self.biases = {}
        self.initialize_layers()

    def initialize_layers(self):
        # Input layer
        self.weights['input'] = 0.1 * np.random.randn(self.input_nodes, self.hidden_nodes)
        self.biases['input'] = 0.1 * np.random.randn(1, self.hidden_nodes)

        # Hidden layer
        self.weights['hidden'] = 0.1 * np.random.randn(self.hidden_nodes, self.output_nodes)
        self.biases['hidden'] = 0.1 * np.random.randn(1, self.output_nodes)        

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