import random
import math

# Load CPI data 
cpi_data = [0.32, 0.24, 0.14, 0.11] # Sample data

# Genetic algorithm parameters
pop_size = 100
num_genes = 2
num_iterations = 50
pc = 0.5 # Crossover probability 
pm = 0.01 # Mutation probability

# Function to evaluate fitness
def evaluate_fitness(individual):
    pred = 0
    for i in range(num_genes):
        pred += individual[i] * cpi_data[-i-1]
    
    error = (pred - cpi_data[-1]) ** 2
    fitness = 1/(error + 0.00001)
    return fitness

# Generate random initial population
def initialize_population():
    population = []
    for i in range(pop_size):
        individual = [random.random() for j in range(num_genes)]
        population.append(individual)
    return population

# Roulette wheel selection
def selection(population):
    fitness_sum = sum([evaluate_fitness(i) for i in population])
    pick = random.uniform(0, fitness_sum)
    current = 0
    for individual in population:
        current += evaluate_fitness(individual)
        if current > pick:
            return individual

# Crossover
def crossover(ind1, ind2):
    # Check if crossover occurs
    if random.random() <= pc:
        child1 = [] 
        child2 = []
        alpha = random.random()
        
        for g1, g2 in zip(ind1, ind2):
            child1.append(alpha*g1 + (1-alpha)*g2)
            child2.append(alpha*g2 + (1-alpha)*g1)
            
        return child1, child2
    else:
        # No crossover, return original individuals
        return ind1, ind2

    
# Mutation    
def mutate(individual):
    for i in range(len(individual)):
        if random.random() < pm:
            individual[i] = random.random()
    return individual

# Generate next generation        
def next_generation(population):
    next_gen = []
    
    # Elitism - carry over best solution
    elite = max(population, key=evaluate_fitness)
    next_gen.append(elite)
    
    while len(next_gen) < pop_size:
        # Selection
        ind1 = selection(population)
        ind2 = selection(population)
        
        # Crossover 
        child1, child2 = crossover(ind1, ind2)
        
        # Mutation
        child1 = mutate(child1)
        child2 = mutate(child2)
        
        # Add to next generation
        next_gen.append(child1)
        next_gen.append(child2)
        
    return next_gen

# Genetic algorithm        
population = initialize_population()
for i in range(num_iterations):
    population = next_generation(population)
    
# Find best solution    
best = max(population, key=evaluate_fitness)
print("Best solution: ", best)
print("Predicted inflation: ", sum([g*c for g,c in zip(best, cpi_data[-num_genes:])]))