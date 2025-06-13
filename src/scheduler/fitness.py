from scheduler import constraints as c
from data import load_data as ld

teams = ld.load_teams()
venues = ld.load_venues()

team_ids = [team["id"] for team in teams]
venue_ids = [venue["id"] for venue in venues]

def fitness(schedule):
    penalty = 0

    venue_time_slots = set() 
    team_time_slots = set()  
    venue_usage = {venue_id: 0 for venue_id in venue_ids}
    team_time = {team_id: [] for team_id in team_ids}
     
    for match in schedule:

        team1_id = match[0]
        team2_id = match[1]
        week = match[2]
        day = match[3]
        time = match[4]
        venue_id = match[5]

        venue_avail = c.venue_availability(venue_id, week, day, time, venue_time_slots)
        team_overlap = c.no_team_overlap(team1_id, team2_id, week, day, time, team_time_slots)
        fair_rest = c.fair_rest_periods(team1_id, team2_id, team_time)

        penalty += (venue_avail + team_overlap + fair_rest)

        venue_time_slots.add((venue_id, week, day, time))
        team_time_slots.add((team1_id, week, day, time))
        team_time_slots.add((team2_id, week, day, time))
        
        venue_usage[venue_id] += 1
        team_time[team1_id].append((team1_id, team2_id, week, day, time))
        team_time[team2_id].append((team1_id, team2_id, week, day, time))


    penalty += c.venue_usage_balance(list(venue_usage.values()))
    
    return penalty
