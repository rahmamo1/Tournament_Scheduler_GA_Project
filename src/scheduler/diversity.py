import random
from scheduler.fitness import fitness
from scheduler.initialization import random_initialization


def hamming_distance(ind1, ind2):
    return sum(i != j for i, j in zip(ind1, ind2))


def crowding(population, offspring, crowding_factor):
    new_population = population.copy()

    for child in offspring:
        candidates = random.sample(new_population, min(crowding_factor, len(new_population)))
        most_similar = min(candidates, key=lambda ind: hamming_distance(child, ind))

        if fitness(child) < fitness(most_similar):
            new_population.remove(most_similar)
            new_population.append(child)

    return new_population


def extinction_restart(
    population, 
    population_size,
    survivor_method,  
    replace_count=None,
    top_n_elitism=None,
    keep_ratio=0.66
):
    num_to_keep = int(population_size * keep_ratio)

    population_sorted = sorted(population, key=fitness)

    method_name = survivor_method.__name__.lower()

    if method_name == "genitor":
        elite_count = replace_count if replace_count else 1

    elif method_name == "elitism":
        elite_count = top_n_elitism if top_n_elitism else 1

    elif method_name == "mu_lambda":
        elite_count = top_n_elitism if top_n_elitism else 1

    else:
        elite_count = 1 

    elite_kept = population_sorted[:elite_count]
    rest_kept = population_sorted[elite_count:num_to_keep]
    new_random = random_initialization(population_size - len(elite_kept) - len(rest_kept))

    new_population = elite_kept + rest_kept + new_random

    return new_population
