from data import load_data as ld

teams = ld.load_teams()
venues = ld.load_venues()

weeks = ["week1", "week2", "week3", "week4", "week5", "week6", "week7"]
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
times = ["01:00-03:00", "03:00-05:00", "05:00-07:00", "07:00-09:00", "09:00-11:00"]


def decode_schedule(schedule):
    decoded_schedule = []
    
    for match in schedule:
        team1_id, team2_id, week_id, day_id, time_id, venue_id = match
        
        team1_name = next((team["name"] for team in teams if team["id"] == team1_id), "Unknown Team")
        team2_name = next((team["name"] for team in teams if team["id"] == team2_id), "Unknown Team")
        
        venue_name = next((venue["name"] for venue in venues if venue["id"] == venue_id), "Unknown Venue")
        
        week_name = weeks[week_id]  
        day_name = days[day_id]    
        time_name = times[time_id] 
        
        decoded_match = [
            team1_name,  
            team2_name,  
            week_name,  
            day_name,   
            time_name,  
            venue_name  
        ]
        
        decoded_schedule.append(decoded_match)
    
    return decoded_schedule

