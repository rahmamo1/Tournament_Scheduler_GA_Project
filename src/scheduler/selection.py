import random
from scheduler.fitness import fitness

def tournament_selection(population, tournament_size):
    tournament_size = min(tournament_size, len(population))
    
    selected_parents = []

    while len(selected_parents) < len(population):  
        tournament_pool = random.sample(population, tournament_size)
        selected_parents.append(min(tournament_pool, key= fitness))
    
    random.shuffle(selected_parents)
    return selected_parents[:len(population) // 2]

def rank_selection(population, rank_size, s=1.5):
  
    s = max(1.0, min(2.0, s))
    
    ranked_population = sorted(population, key=fitness)
    mu = len(ranked_population)
    
    selection_probs = []
    for i, ind in enumerate(ranked_population):
        rank = i + 1 
        prob = (2 - s)/mu + (2 * (mu - rank) * (s - 1)) / (mu * (mu - 1))
        selection_probs.append(prob)
    
    selected_parents = random.choices(
        ranked_population,
        weights=selection_probs,
        k=rank_size
    )
    
    return selected_parents


def over_selection(population):

    #80% of parents are chosen from the top x% of individuals.
    #20% of parents are chosen from the rest.

    num_selected=None
    if num_selected is None:
        num_selected = len(population) // 2
    
    pop_size = len(population)
    
    # Determine x% based on population size
    if pop_size >= 8000:
        x_percent = 0.04
    elif pop_size >= 4000:
        x_percent = 0.08
    elif pop_size >= 2000:
        x_percent = 0.16
    elif pop_size >= 1000:
        x_percent = 0.32
    else:
        x_percent = 0.5
    
    ranked_population = sorted(population, key=fitness)
    
    cutoff = max(1, int(pop_size * x_percent))
    top_group = ranked_population[:cutoff]
    rest_group = ranked_population[cutoff:]

    num_top = int(num_selected * 0.8)
    num_rest = num_selected - num_top

    selected_top = random.choices(top_group, k=num_top)
    selected_rest = random.choices(rest_group, k=num_rest) if rest_group else []

    return selected_top + selected_rest

