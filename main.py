from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players
import matplotlib.pyplot as plt

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

# Trim the data frame to remove any duplicate seasons.
career_df = career_df.drop_duplicates(subset='SEASON_ID', keep='last')

# Calculate a player's PIE (Player Impact Estimate) for each season, rounded to 3 decimal places.
career_df['PIE'] = (career_df['PTS'] + career_df['AST'] + career_df['REB'] + career_df['STL'] + career_df['BLK'] - career_df['FGA'] - career_df['FTA'] - career_df['TOV'] - career_df['PF']) / (career_df['PTS'] + career_df['AST'] + career_df['REB'] + career_df['STL'] + career_df['BLK'] + career_df['FGA'] + career_df['FTA'] + career_df['TOV'] + career_df['PF']).round(3)

# Convert percentage columns to actual percentages.
career_df['FG_PCT'] = (career_df['FG_PCT'] * 100).round(1).astype(str) + "%"
career_df['FG3_PCT'] = (career_df['FG3_PCT'] * 100).round(1).astype(str) + "%"
career_df['FT_PCT'] = (career_df['FT_PCT'] * 100).round(1).astype(str) + "%"

# Calculate points per game, assists per game, etc.
career_df['PPG'] = (career_df['PTS'] / career_df['GP']).round(1)
career_df['APG'] = (career_df['AST'] / career_df['GP']).round(1)
career_df['RPG'] = (career_df['REB'] / career_df['GP']).round(1)
career_df['SPG'] = (career_df['STL'] / career_df['GP']).round(1)
career_df['BPG'] = (career_df['BLK'] / career_df['GP']).round(1)

# Print the player's career stats.
print(career_df[['SEASON_ID', 'TEAM_ABBREVIATION', 'GP', 'GS', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PPG', 'APG', 'RPG', 'SPG', 'BPG', 'PIE']])

# Plot the player's PPG, APG, and BPG as three separate graphs.
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8))

# PPG graph
ax1.plot(career_df['SEASON_ID'], career_df['PPG'], marker='o')
ax1.set_xlabel('Season')
ax1.set_ylabel('PPG')
ax1.set_title('Points Per Game')

# APG graph
ax2.plot(career_df['SEASON_ID'], career_df['APG'], marker='o')
ax2.set_xlabel('Season')
ax2.set_ylabel('APG')
ax2.set_title('Assists Per Game')

# BPG graph
ax3.plot(career_df['SEASON_ID'], career_df['BPG'], marker='o')
ax3.set_xlabel('Season')
ax3.set_ylabel('BPG')
ax3.set_title('Blocks Per Game')

# Display all graphs
plt.tight_layout()
plt.show()