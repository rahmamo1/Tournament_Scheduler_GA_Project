import random
from data import load_data as ld
from scheduler.representation import permutation_representation
from scheduler.representation import encode
teams = ld.load_teams()
venues = ld.load_venues()


weeks = ["week1" , "week2" , "week3" , "week4"  , "week5" , "week6" , "week7"]
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
times = ["01:00-03:00","03:00-05:00", "05:00-07:00", "07:00-09:00", "09:00-11:00"]
timeslots = [(week, day, time) for week in weeks for day in days for time in times]

def random_initialization(num_individuals , seed=None):

    if seed is not None:
        random.seed(seed)

    population = []
    venue_ids = [venue["id"] for venue in venues]

    for _ in range(num_individuals):
        schedule = []
        team_pairs = permutation_representation()

        for pair in team_pairs:
            week = random.choice(weeks)
            day = random.choice(days)
            time = random.choice(times)
            encoded_week, encoded_day, encoded_time = encode(week, day, time)
            venue = random.choice(venue_ids)

            match = [
                pair[0],           
                pair[1],           
                encoded_week,
                encoded_day,
                encoded_time,
                venue
            ]
            schedule.append(match)

        population.append(schedule)

    return population


def greedy_initialization(num_individuals , seed=None ):

    if seed is not None:
        random.seed(seed)

    population = []
    venue_ids = [venue["id"] for venue in venues]

    for _ in range(num_individuals):
        schedule = []
        venue_slots = set()
        team_weekly_matches = {}
        team_slots = set()
        week_match_count = {week: 0 for week in weeks}  

        day_count = {day: 0 for day in days}          
        time_count = {time: 0 for time in times}      
        venue_count = {venue: 0 for venue in venue_ids} 

        team_pairs = permutation_representation()

        for team1_id, team2_id in team_pairs:
            best_slot = None
            best_score = None

            sorted_weeks = sorted(weeks, key=lambda w: week_match_count[w])

            for week in sorted_weeks:
                for day in days:
                    for time in times:
                        for venue in venue_ids:
                            encoded_week, encoded_day, encoded_time = encode(week, day, time)
                            slot = (encoded_week, encoded_day, encoded_time, venue)

                            if (
                                slot not in venue_slots and
                                (team1_id, encoded_week, encoded_day, encoded_time) not in team_slots and
                                (team2_id, encoded_week, encoded_day, encoded_time) not in team_slots
                            ):
                                score = day_count[day] + time_count[time] + venue_count[venue]

                                if best_slot is None or score < best_score:
                                    best_slot = (week, day, time, venue)
                                    best_score = score

            if best_slot:
                week, day, time, venue = best_slot
                encoded_week, encoded_day, encoded_time = encode(week, day, time)

                match = [team1_id, team2_id, encoded_week, encoded_day, encoded_time, venue]
                schedule.append(match)

                venue_slots.add((encoded_week, encoded_day, encoded_time, venue))
                team_slots.add((team1_id, encoded_week, encoded_day, encoded_time))
                team_slots.add((team2_id, encoded_week, encoded_day, encoded_time))

                team_weekly_matches.setdefault(team1_id, set()).add(week)
                team_weekly_matches.setdefault(team2_id, set()).add(week)
                week_match_count[week] += 1  

                day_count[day] += 1
                time_count[time] += 1
                venue_count[venue] += 1

        population.append(schedule)

    return population
