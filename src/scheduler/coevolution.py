import random
from scheduler.fitness import fitness

def initialize_islands(num_islands, population_size, init_function):
    return [init_function(population_size) for _ in range(num_islands)]

def migrate_islands(islands, migration_rate=0.01, elite=True):
    num_islands = len(islands)
    island_size = len(islands[0])
    migrants_per_island = max(1, int(island_size * migration_rate))

    for i in range(num_islands):
        source = islands[i]
        target = islands[(i + 1) % num_islands]

        if elite:
            source.sort(key=lambda x: fitness(x))  # keep lowest penalty (best)
            migrants = source[:migrants_per_island]
        else:
            migrants = random.sample(source, migrants_per_island)

        target.sort(key=lambda x: fitness(x), reverse=True)  # remove worst
        target[-migrants_per_island:] = migrants

