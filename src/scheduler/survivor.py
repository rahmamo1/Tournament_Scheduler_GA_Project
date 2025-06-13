from scheduler.fitness import fitness


def elitism(population, offspring, top_n=None):

    if top_n is None:
        top_n = 5
        
    combined_population = population + offspring
    sorted_population = sorted(combined_population, key=fitness)

    best_individuals = sorted_population[:top_n]
    
    return best_individuals


def genitor (population, offspring, replace_count=None):
    
    if replace_count is None:
        replace_count = len(offspring)

    replace_count = min(replace_count, len(population))
    
    sorted_population = sorted(population, key=fitness)
    survivors = sorted_population[:-replace_count]

    next_generation = survivors + offspring

    return next_generation

def mu_lambda(parents, offspring, mu=None, top_n=None):
    if mu is None:
        mu = top_n if top_n is not None else len(parents)
    
    if not offspring:
        return parents[:mu] if parents else []
    
    sorted_offspring = sorted(offspring, key=fitness)
    
    next_generation = sorted_offspring[:min(mu, len(offspring))]
    
    return next_generation
