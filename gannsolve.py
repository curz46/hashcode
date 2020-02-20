import random
import math
import operator

from objects import *

params = {
    "generation_size": 50,
    "prune": 45,
    "elitism_keep": 2,
    "mutation_chance": 0.03
}

current_topology = [4,8,10,4,1]

def train(scenario):
    pass

def gen_output_file(trained_net, scenario):
    for lib in scenario.libraries:
        score = trained_net.eval_library(lib, scenario.days)
        lib.gann_score = score
    
    scenario.libraries.sort(key=operator.attrgetter('gann_score'), reverse=True)

    outfile = open("gann_outfile.txt", 'w+')
    outfile.write("{0}\n".format(len(scenario.libraries)))
    for library in scenario.libraries:
        outfile.write("{0} {1}\n".format(library.id, len(library.books)))
        for book in library.books:
            outfile.write("{0} ".format(book.id))
        outfile.write("\n")
    

class GeneticAlgorithm:
    @staticmethod
    def crossover():
        newGen = []
        for i in range(params["generation_keep"]):
            newGen.append(currentGen[i])

        topology = currentGen[0].topology
        layers = len(currentGen[0].layers)

        while len(newGen) < params["generation_size"]:
            weights = []

            nn_one = random.choice(currentGen)
            nn_two = random.choice(currentGen)
            while nn_one == nn_two:
                nn_one = random.choice(currentGen)
                nn_two = random.choice(currentGen)
            
            for layer_idx in range(layers):
                nn_one_layer = nn_one.layers[layer_idx]
                nn_two_layer = nn_two.layers[layer_idx]
                
                weights.append([])

                for in_node in len(nn_one_layer.neurons):
                    weights[layer_idx].append([])
                    for out_node in len(nn_one_layer.output_neurons):
                        weights[layer_idx][in_node].append(random.choice([nn_one_layer.weights[in_node][out_node],nn_two_layer.weights[in_node][out_node]]))
            
            newGen.append(NeuralNetwork(topology, weights))

    @staticmethod
    def mutate(currentGen):
        for nn in currentGen:
            for nn_layer in nn.layers:
                for in_node in range(nn_layer.neurons):
                    for out_node in range(nn_layer.output_neurons):
                        nn_layer.weights[in_node][out_node] = random.uniform(-1,1)
    
    @staticmethod
    def evolve(currentGen):
        currentGen = currentGen[:params["prune"]]

        newGen = crossover(currentGen)

        newGen = mutate(currentGen)

        return newGen


class NeuralNetwork:
    def __init__(self, topology, weights=[]):
        self.topology = topology
        self.layers = []
        self.weights = weights
        self.init_layers()

    def init_layers(self):
        for i in range(len(self.topology) - 1):
            layer = None
            if len(self.weights) > 0:
                layer = NeuralLayer(self.topology[i], self.topology[i + 1], self.weights[i])
            else:
                layer = NeuralLayer(self.topology[i], self.topology[i + 1], [])
            self.layers.append(layer)
    
    def eval_library(self, library, days):
        total_sum = 0
        for book in library.books:
            total_sum += book.score
        
        time_to_process = math.ceil(len(library.books) / library.books_per_day)

        return self.evaluate([total_sum, library.signup_time, time_to_process, days])

    
    def evaluate(self, inputs):
        for layer in self.layers:
            inputs = layer.evaluate(inputs)
        
        return inputs

class NeuralLayer:
    def __init__(self, neurons, output_neurons, weights):
        self.neurons = neurons
        self.output_neurons = output_neurons
        self.weights = weights
        if len(weights) == 0:
            self.random_weights()
    
    def random_weights(self):
        for i in range(self.neurons):
            self.weights.append([])
            for j in range(self.output_neurons):
                self.weights[i].append(random.uniform(-1,1))

    def evaluate(self, inputs):
        outputs = [0.0] * self.output_neurons
        for i in range(self.neurons):
            for j in range(self.output_neurons):
                outputs[j] += inputs[i] * self.weights[i][j]
        
        for i in range(len(outputs)):
            outputs[i] = math.tanh(outputs[i])

        return outputs