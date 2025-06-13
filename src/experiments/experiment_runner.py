
import random 
def cyclic_crossover(parent1, parent2):
    size = len(parent1)
    child1 = [None] * size
    child2 = [None] * size

    visited = [False] * size

    cycle = 0
    while any(not visited[i] for i in range(size)): 
        current_idx = 0

        while visited[current_idx]:
            current_idx += 1

        cycle_start = current_idx
        while not visited[cycle_start]:
            if cycle % 2 == 0:
                child1[cycle_start] = parent1[cycle_start]
                child2[cycle_start] = parent2[cycle_start]
            else:
                child1[cycle_start] = parent2[cycle_start]
                child2[cycle_start] = parent1[cycle_start]

            visited[cycle_start] = True
            cycle_start = parent2.index(parent1[cycle_start])  

        cycle += 1

    return child1, child2



parent1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
parent2 = [9, 3, 7, 8, 2, 6, 5, 1, 4]

child1, child2 = cyclic_crossover(parent1, parent2)

print("Parent 1:", parent1)
print("Parent 2:", parent2)
print("Child 1:", child1)
print("Child 2:", child2)


#========================================
from scheduler import constraints as c
from data import load_data as ld

teams = ld.load_teams()
venues = ld.load_venues()

def fitness(schedule):
    penalty = 0

    venue_time_slots = set() 
    team_time_slots = set()  
    venue_usage = {venue["name"]: 0 for venue in venues} 
    team_time = {team["name"]: [] for team in teams} 

    for match in schedule:
        team1 = match["team1"]
        team2 = match["team2"]
        day = match["day"]
        timeslot = match["time"]
        venue_name = match["venue"]

        venue_avail = c.venue_availability(venue_name, day, timeslot, venue_time_slots)
        team_overlap = c.no_team_overlap(team1, team2, day, timeslot, team_time_slots)
        fair_rest = c.fair_rest_periods(team1, team2, team_time)

        penalty += (venue_avail + team_overlap + fair_rest)

        venue_time_slots.add((venue_name, day, timeslot))
        team_time_slots.add((team1, day, timeslot))
        team_time_slots.add((team2, day, timeslot))
        
        venue_usage[venue_name] += 1
        team_time[team1].append(match)
        team_time[team2].append(match)

    penalty += c.venue_usage_balance(list(venue_usage.values()))
    
    return penalty


