import random
from data import load_data as ld
teams = ld.load_teams()
venues = ld.load_venues()

def is_valid(schedule):
    used_slots = set()
    team_slots = set()

    for match in schedule:
        team1, team2, week, day, time, venue = match
        slot = (week, day, time, venue)

        if slot in used_slots:
            return False
        used_slots.add(slot)

        team1_slot = (team1, week, day, time)
        team2_slot = (team2, week, day, time)

        if team1_slot in team_slots or team2_slot in team_slots:
            return False
        team_slots.add(team1_slot)
        team_slots.add(team2_slot)

    return True

def swap_mutation(schedule):
    mutated = [match.copy() for match in schedule] 
    
    idx1 = random.randint(0, len(mutated) - 1)
    idx2 = random.randint(0, len(mutated) - 1)
    while idx1 == idx2:
        idx2 = random.randint(0, len(mutated) - 1)

    mutated[idx1][2], mutated[idx2][2] = mutated[idx2][2], mutated[idx1][2]  # week
    mutated[idx1][3], mutated[idx2][3] = mutated[idx2][3], mutated[idx1][3]  # day
    mutated[idx1][4], mutated[idx2][4] = mutated[idx2][4], mutated[idx1][4]  # time
    mutated[idx1][5], mutated[idx2][5] = mutated[idx2][5], mutated[idx1][5]  # venue

    if is_valid(mutated):
        return mutated
    else:
        return schedule

def scramble_mutation(schedule):
    mutated = [match.copy() for match in schedule]
    size = len(mutated)
    if size < 2:
        return mutated

    start = random.randint(0, size - 2)
    end = random.randint(start + 1, size - 1)

    slots = [match[2:] for match in mutated[start:end + 1]]
    random.shuffle(slots)

    for i, slot in enumerate(slots):
        mutated[start + i][2:] = slot

    if is_valid(mutated):
        return mutated
    else:
        return schedule


def inversion_mutation(schedule):
    mutated = [match.copy() for match in schedule]
    size = len(mutated)
    if size < 2:
        return mutated

    start = random.randint(0, size - 2)
    end = random.randint(start + 1, size - 1)

    slots = [match[2:] for match in mutated[start:end + 1]]
    reversed_slots = list(reversed(slots))

    for i, slot in enumerate(reversed_slots):
        mutated[start + i][2:] = slot

    if is_valid(mutated):
        return mutated
    else:
        return schedule
