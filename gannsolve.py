import random
import math

class GeneticAlgorithm:
    @staticmethod
    def crossover(currentGen)

class NeuralNetwork:
    def __init__(self, topology):
        self.topology = topology
        self.layers = []
        self.init_layers()

    def init_layers(self):
        for i in range(self.topology - 1)
            layer = NeuralLayer(self.topology[i], self.topology[i + 1])
            self.layers.append(layer)
    
    def evaluate(self, inputs):
        for layer in self.layers:
            inputs = layer.evaluate(inputs)
        
        return inputs

class NeuralLayer:
    def __init__(self, neurons, output_neurons, weights=[]):
        self.neurons = neurons
        self.output_neurons = output_neurons
        self.weights = weights
        if weights == []:
            self.random_weights()
    
    def random_weights(self):
        for i in range(self.neurons):
            weights.append([])
            for j in range(self.output_neurons):
                weights.append(random.random(-1,1))

    def evaluate(self, inputs):
        outputs = [0.0] * self.output_neurons
        for i in range(self.neurons):
            for j in range(self.output_neurons):
                outputs[i] += inputs * self.weights[i][j]
        
        for i in range(outputs):
            outputs[i] = math.tanh(outputs[i])

        return outputs