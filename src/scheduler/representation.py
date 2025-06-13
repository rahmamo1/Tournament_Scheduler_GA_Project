import random
from data import load_data as ld

teams = ld.load_teams()
venues = ld.load_venues()

weeks = ["week1", "week2", "week3", "week4", "week5", "week6", "week7"]
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
times = ["01:00-03:00", "03:00-05:00", "05:00-07:00", "07:00-09:00", "09:00-11:00"]


def encode(week, day, time):
    
    if week not in weeks:
        raise ValueError(f"Invalid week: {week}. Valid weeks are: {weeks}")
    if day not in days:
        raise ValueError(f"Invalid day: {day}. Valid days are: {days}")
    if time not in times:
        raise ValueError(f"Invalid time: {time}. Valid times are: {times}")

    week_index = weeks.index(week)  
    day_index = days.index(day)    
    time_index = times.index(time)   
    
    return (week_index, day_index, time_index)


def permutation_representation():

    team_ids = [team["id"] for team in teams]

    team_pairs = [[team_ids[i], team_ids[j]] for i in range(len(team_ids)) for j in range(i + 1, len(team_ids))]

    random.shuffle(team_pairs)

    #chromosome be like [[1, 4], [2, 5], [3, 6], ...]

    return team_pairs





