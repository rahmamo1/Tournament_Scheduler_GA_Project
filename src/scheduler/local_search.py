import random
from scheduler.fitness import fitness

def local_search_refined(schedule, max_iterations = 50, neighborhood_size = 5):
    best_schedule = schedule.copy()
    best_penalty = fitness(best_schedule)
    
    for _ in range(max_iterations):
        # Generate neighborhood by small perturbations
        neighbors = []
        for _ in range(neighborhood_size):
            temp_schedule = best_schedule.copy()
            
            # Apply different types of perturbations
            if len(temp_schedule) > 1:
                # Swap mutation
                idx1, idx2 = random.sample(range(len(temp_schedule)), 2)
                temp_schedule[idx1], temp_schedule[idx2] = temp_schedule[idx2], temp_schedule[idx1]
                
                neighbors.append(temp_schedule)
        
        # Evaluate all neighbors
        for neighbor in neighbors:
            neighbor_penalty = fitness(neighbor)
            if neighbor_penalty < best_penalty:
                best_schedule = neighbor.copy()
                best_penalty = neighbor_penalty
                
    return best_schedule
