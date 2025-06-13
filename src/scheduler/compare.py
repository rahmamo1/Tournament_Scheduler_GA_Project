import pandas as pd
from scheduler.fitness import fitness
from scheduler.decode import decode_schedule

def compare_random_vs_optimized(random_schedule,optimized_schedule):
    random_penalty = fitness(random_schedule)
    optimized_penalty = fitness(optimized_schedule)

    decoded_random_schedule = decode_schedule(random_schedule)
    decoded_optimized_schedule = decode_schedule(optimized_schedule)

    random_schedule_data=[{

        "Team 1": match[0],
        "Team 2": match[1],
        "Week": match[2],
        "Day": match[3],
        "Time": match[4],
        "Venue": match[5]

    }for match in decoded_random_schedule]

    optimized_schedule_data=[{

        "Team 1": match[0],
        "Team 2": match[1],
        "Week": match[2],
        "Day": match[3],
        "Time": match[4],
        "Venue": match[5]

    }for match in decoded_optimized_schedule]

    random_schedule_df = pd.DataFrame(random_schedule_data)
    optimized_schedule_df = pd.DataFrame(optimized_schedule_data)

    comparison_result={
        "Random Schedule Penalty": random_penalty,
        "Optimized Schedule Penalty": optimized_penalty,
        "Improvement in Penalty": random_penalty - optimized_penalty,
        "Random Schedule Data": random_schedule_df,
        "Optimized Schedule Data": optimized_schedule_df
    }

    return comparison_result