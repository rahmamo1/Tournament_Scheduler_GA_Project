import random
import math
import time
from scheduler.initialization import random_initialization
from scheduler.fitness import fitness
from scheduler.diversity import crowding, extinction_restart
from scheduler.termination import max_generations_reached, target_fitness_reached, time_limit_exceeded
from scheduler.coevolution import initialize_islands, migrate_islands 
from scheduler.local_search import local_search_refined

def genetic_algorithm(
    population_size,
    generations,
    crossover_method,
    mutation_method,
    initial_mutation_rate,
    crossover_probability,
    tournament_size=None,
    top_n_elitism=None,
    rank_size=None,
    replace_count=None,
    selection_method=None,
    survivor_method=None,
    initial_population=None,
    stagnation_limit=25,
    diversity_method=None,
    crowding_factor=None,
    extinction_keep_ratio=None,
    time_limit_minutes: float = None,
    target_fitness=0,
    local_search_probability=0.3,  
    local_search_on_offspring=False,  
    local_search_on_individuals=True, 
    local_search_interval=5 ,
    seed=None
):
    if seed is not None:
        random.seed(seed)

    num_islands = 5
    island_size = population_size // num_islands
    if initial_population is not None:
        init_function = lambda size: initial_population
    else:
        init_function = random_initialization

    islands = initialize_islands(num_islands, island_size, init_function)

    start_time = time.time()
    time_limit_seconds = time_limit_minutes * 60 if time_limit_minutes else None

    penalties_per_generation = []
    mutation_rate = initial_mutation_rate

    best_solution_ever = None
    best_penalty_ever = float("inf")
    generations_without_improvement = 0
    generation = 0
    fitness_history = []

    MIGRATION_INTERVAL = 25

    while True:
        terminate = False
        if time_limit_minutes is not None and time_limit_exceeded(start_time, time_limit_seconds):
            print(f"Terminating: Time limit of {time_limit_minutes} minutes reached")
            terminate = True
        if target_fitness is not None and target_fitness_reached(best_penalty_ever, target_fitness):
            print(f"Terminating: Target fitness {target_fitness} achieved")
            terminate = True
        if max_generations_reached(generation, generations):
            print("Terminating: Maximum generations reached")
            terminate = True
        if terminate:
            break

        for i in range(num_islands):
            population = islands[i]
            offspring = []
            penalties = [fitness(schedule) for schedule in population]
            current_best_penalty = min(penalties)
            fitness_history.append(current_best_penalty)
            current_best_idx = penalties.index(current_best_penalty)
            current_best_solution = population[current_best_idx]
            worst_penalty = max(penalties)

            if current_best_penalty < best_penalty_ever:
                best_penalty_ever = current_best_penalty
                best_solution_ever = current_best_solution.copy()
                generations_without_improvement = 0
            else:
                generations_without_improvement += 1

            penalties_per_generation.append(best_penalty_ever)

            print(f"[Island {i+1}] Generation {generation}: Best = {current_best_penalty}, Worst = {worst_penalty}, Best Ever = {best_penalty_ever}, Stagnation = {generations_without_improvement}")

            mutation_rate = min(0.4, mutation_rate * 1.05) if generations_without_improvement > stagnation_limit else max(0.05, mutation_rate * 0.98)
            print(f"[Island {i+1}] Mutation rate: {mutation_rate:.2f}")

            # Apply local search to individuals periodically
            if local_search_on_individuals and generation % local_search_interval == 0:
                for idx in range(len(population)):
                    if random.random() < local_search_probability:
                        population[idx] = local_search_refined(population[idx])
                print(f"[Island {i+1}] Applied local search to individuals")

            if generations_without_improvement >= stagnation_limit:
                if diversity_method in ["Extinction", "Both"]:
                    population = extinction_restart(
                        population=population,
                        population_size=island_size,
                        survivor_method=survivor_method,
                        replace_count=replace_count,
                        top_n_elitism=top_n_elitism,
                        keep_ratio=extinction_keep_ratio
                    )
                    generations_without_improvement = 0
                    print(f"[Island {i+1}] Extinction restart applied!")

            sorted_population = [x for _, x in sorted(zip(penalties, population), key=lambda pair: pair[0])]
            
            if survivor_method.__name__ == "genitor":
                elite_individuals = survivor_method(sorted_population, offspring, replace_count=replace_count)
            elif survivor_method.__name__ == "mu_plus_lambda_selection":
                elite_individuals = survivor_method(sorted_population, offspring, mu=top_n_elitism)
            else:  # Default to elitism
                elite_individuals = survivor_method(sorted_population, offspring, top_n=top_n_elitism)

            if selection_method.__name__ == "tournament_selection":
                selected_parents = selection_method(population, tournament_size=tournament_size)
            elif selection_method.__name__ == "rank_selection":
                selected_parents = selection_method(population, rank_size=rank_size , s=1.5)
            elif selection_method.__name__ == "over_selection":
                selected_parents = selection_method(population)

            parent_idx = 0
            while len(offspring) < island_size - len(elite_individuals) and parent_idx + 1 < len(selected_parents):
                parent1, parent2 = selected_parents[parent_idx], selected_parents[parent_idx + 1]
                parent_idx += 2
                children = []
                if random.random() < crossover_probability:
                    children.extend([crossover_method(parent1, parent2), crossover_method(parent2, parent1)])
                else:
                    children.extend([parent1.copy(), parent2.copy()])

                for child in children:
                    if random.random() < mutation_rate:
                        mutated_child = mutation_method(child)
                        offspring.append(mutated_child)
                    else:
                        offspring.append(child)

                    # Apply local search to offspring
                    if local_search_on_offspring and random.random() < local_search_probability:
                        improved_child = local_search_refined(child)
                        offspring[-1] = improved_child  # Replace the last added child with the improved version

            if diversity_method in ["Crowding", "Both"] and generation % 25 == 0:
                population = crowding(population, offspring, crowding_factor=crowding_factor)
            else:
                population = elite_individuals + offspring

            population = population[:island_size]

            islands[i] = population

        if generation % MIGRATION_INTERVAL == 0:
            migrate_islands(islands, migration_rate=0.1, elite=True)
            print(f"Migration done at generation {generation}")

        generation += 1

    final_population = [ind for island in islands for ind in island]
    final_sorted_population = sorted(final_population, key=fitness)

    if best_solution_ever is not None and best_penalty_ever < fitness(final_sorted_population[0]):
        if not any(fitness(ind) == best_penalty_ever for ind in final_sorted_population):
            final_sorted_population.insert(0, best_solution_ever)
            final_sorted_population = final_sorted_population[:population_size]

    return final_sorted_population, penalties_per_generation