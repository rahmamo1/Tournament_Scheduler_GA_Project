import random
from data import load_data as ld
from scheduler.representation import encode

teams = ld.load_teams()
venues = ld.load_venues()

weeks = ["week1", "week2", "week3", "week4", "week5", "week6", "week7"]
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
times = ["01:00-03:00", "03:00-05:00", "05:00-07:00", "07:00-09:00", "09:00-11:00"]

def order_crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(len(parent1)), 2))

    child = [None] * size
    child[start:end + 1] = parent1[start:end + 1]

    p2_idx = (end + 1) % len(parent2)
    c_idx = (end + 1) % len(child)

    safety_counter = 0
    max_safety = size * 2
    
    none_count = child.count(None)
    while none_count > 0 and safety_counter < max_safety:
        match = parent2[p2_idx]

        if (match[0], match[1]) not in [(m[0], m[1]) for m in child if m is not None]:

            child[c_idx] = match
            none_count -= 1
        p2_idx = (p2_idx + 1) % len(parent2)
        c_idx = (c_idx + 1) % len(child)
        safety_counter += 1
    
    if none_count > 0:
        for i in range(len(child)):
            if child[i] is None:

                team_ids = [team["id"] for team in teams]
                team_pairs = [[team_ids[i], team_ids[j]] for i in range(len(team_ids)) for j in range(i + 1, len(team_ids))]
                random.shuffle(team_pairs)
                
                for team1_id, team2_id in team_pairs:
                    if not any(m is not None and m[0] == team1_id and m[1] == team2_id for m in child):
                        venue_ids = [venue["id"] for venue in venues]
                        venue = random.choice(venue_ids)
                        
                        week, day, time = random.choice(weeks), random.choice(days), random.choice(times)
                        encoded_week, encoded_day, encoded_time = encode(week, day, time)
                        
                        child[i] = [
                            team1_id,  
                            team2_id,  
                            encoded_week,  
                            encoded_day,  
                            encoded_time,  
                            venue
                        ]
                        break

    if None in child:
        from scheduler.initialization import random_initialization
        return random_initialization(1)[0]
    
    try:
        assert len(set(tuple(match) for match in child)) == len(child), "Duplicated or missing matches in child"
    except (AssertionError, AttributeError):
        return parent1.copy()

    return child


def cyclic_crossover (parent1, parent2):
    size = len(parent1)
    child = [None] * size  

    if None in parent1 or None in parent2:
        return parent1.copy() if None not in parent1 else parent2.copy()

    try:
        visited = [False] * size  
        cycle = 0  
        
        while any(not visited[i] for i in range(size)): 
            current_idx = visited.index(False)  
            indices_in_cycle = []  
            
            while not visited[current_idx]: 
                indices_in_cycle.append(current_idx)
                visited[current_idx] = True
                
                try:
                    current_idx = parent2.index(parent1[current_idx])  
                except ValueError:
                    unvisited = [i for i, v in enumerate(visited) if not v]
                    current_idx = unvisited[0] if unvisited else -1
                    break

           
            if cycle % 2 == 0:
                for idx in indices_in_cycle:
                    child[idx] = parent1[idx]
            else:
                for idx in indices_in_cycle:
                    child[idx] = parent2[idx]

            cycle += 1

        if None in child:
            return parent1.copy()  
        return child 
            
    except Exception:
        return parent1.copy()


def partially_mapped_crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))  

    child = [None] * size
    mapping = {}

    for i in range(start, end + 1):
        child[i] = parent1[i]  
        key = tuple(parent2[i][:2])  
        val = tuple(parent1[i][:2]) 
        mapping[key] = val

    for i in range(size):
        if i >= start and i <= end:
            continue

        candidate = parent2[i][:2]  
        candidate_key = tuple(candidate)  

        while candidate_key in mapping: 
            candidate_key = mapping[candidate_key]

        match = next((m for m in parent1 + parent2 if tuple(m[:2]) == candidate_key), None)
        child[i] = match  

    for i in range(size):
        if child[i] is not None:
            child[i] = child[i][:6]    
            
    if None in child:
        from scheduler.initialization import random_initialization
        return random_initialization(1)[0]

    try:
        assert len(set(tuple(match[:2]) for match in child)) == len(child), "Duplicated or missing matches in child"
    except (AssertionError, AttributeError):
        return parent1.copy() 

    return child  