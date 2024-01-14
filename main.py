from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players

# Get all players.
player_dict = players.get_players()

names = [player['full_name'] for player in player_dict]

selected_player = input("Enter a player's name: ")


# Check if there are multiple players with the same name.
players = [player for player in player_dict if player['full_name'].lower() == selected_player.lower()]

if len(players) > 1:
    print("There are multiple players with the same name. Please select one of the following:")
    print(players[0])
    for i in range(len(players)):
        career = playercareerstats.PlayerCareerStats(player_id=players[i]['id'])
        career_df = career.get_data_frames()[0]
        career_started = career_df['SEASON_ID'].iloc[0]
        career_ended = career_df['SEASON_ID'].iloc[-1]
        print(f"{i+1}. {players[i]['full_name']} played between {career_started} and {career_ended}")
    player_index = int(input("Enter the number of the player you want: "))
    player_id = players[player_index-1]['id']
else:
    player_id = players[0]['id']
    
range_start = input("Enter a start year: ")
range_end = input("Enter an end year: ")

# Get player's stats between the given years.
career = playercareerstats.PlayerCareerStats(player_id=player_id)
career_df = career.get_data_frames()[0]
career_df = career_df[career_df['SEASON_ID'].between(range_start, range_end)]

# Add a column for the player's PIE
#career_df['PIE'] = 0.0

# Calculate a player's PIE (Player Impact Estimate) for each season, rounded to 3 decimal places.
career_df['PIE'] = (career_df['PTS'] + career_df['AST'] + career_df['REB'] + career_df['STL'] + career_df['BLK'] - career_df['FGA'] - career_df['FTA'] - career_df['TOV'] - career_df['PF']) / (career_df['PTS'] + career_df['AST'] + career_df['REB'] + career_df['STL'] + career_df['BLK'] + career_df['FGA'] + career_df['FTA'] + career_df['TOV'] + career_df['PF']).round(3)

# Neatly print the player's important stats in the form of a table in the following format: Year in the league, Season, Team name, Games Played, Games Started, Minutes Played, Field Goals Made, FGA, FGM, FG%, 3PA, 3PM, 3PT%, FTM, FTA, FT%, OREB, DREB, REB, AST, STL, BLK, TOV, PF, PTS, PIE
print(career_df[['SEASON_ID', 'TEAM_ABBREVIATION', 'GP', 'GS', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'PIE']])

def season(player_id):
    season = input("Enter the year the season started in: ")
    span = int(input("1 - Regular Season\n2 - Playoffs\n3 - Both\nEnter the number of the span you want: "))
    career = playercareerstats.PlayerCareerStats(player_id=player_id)
    career_df = career.get_data_frames()[0]
    


    