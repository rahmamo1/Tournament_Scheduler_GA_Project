#(Direct = hard enforcement | Indirect = soft penalties for optimization)

def venue_availability(venue_id, week, day, time, venue_time_slots):
    # Direct (hard constraint) - enforce feasibility
    if (venue_id, week , day, time) in venue_time_slots:
        return 100  # large penalty for infeasibility
    return 0
        

def no_team_overlap(team1_id, team2_id, week , day, time, team_time_slots):
    if (team1_id, week, day, time) in team_time_slots or (team2_id, week, day, time) in team_time_slots:
        return 100  # large penalty for infeasibility
    return 0



def venue_usage_balance(venue_usage):
    # Indirect (soft constraint) - optimize for balance
    imbalance = max(venue_usage) - min(venue_usage)
    if imbalance > 3 :
        penalty = imbalance * 5  # scaled soft penalty
        
    else:
        penalty = 0

    return penalty

def fair_rest_periods(team1_id, team2_id, team_time):
    def get_last_two_weeks(team_id):
        weeks = [match[2] for match in team_time.get(team_id, []) if isinstance(match[2], int)]
        if len(weeks) < 2:
            return None  
        return sorted(weeks)[-2:]

    penalty = 0

    for team_id in [team1_id, team2_id]:
        last_two = get_last_two_weeks(team_id)
        if last_two:
            rest = last_two[1] - last_two[0]
            if rest < 2:  
                penalty += (2 - rest) * 5  

    return penalty

