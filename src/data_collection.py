import pandas as pd
from yahoo_fantasy_api import League, Team

curr_season_code = 461

def get_player_stats(league, player_name):
    player_details = pd.json_normalize(league.player_details(player_name))
    player_id = player_details['player_id'].tolist()
    player_stats = league.player_stats(player_id, req_type='season', season=2025)
    player_stats = pd.json_normalize(player_stats)
    # print(player_stats._get_value(0, 'Pass TD'))
    return player_stats

def get_team_from_num(oauth, curr_week, team_num):
    if team_num > 12 or team_num < 1:
        return "Invalid team number"
    team_code = str(curr_season_code) + ".l.6288.t." + str(team_num)
    team = Team(oauth, team_key=team_code)
    roster = team.roster(curr_week)
    return pd.json_normalize(roster)

def get_team_yearly_stats(league, team):
    player_id_list = team['player_id'].tolist()
    team_stats_json = league.player_stats(player_id_list, req_type='season', season=2025)
    team_stats = pd.json_normalize(team_stats_json)
    team_stats.fillna(0, inplace=True)
    team_stats['total_points'] = pd.to_numeric(team_stats['total_points'])
    eligible_pos = team['eligible_positions']
    selected_pos = team['selected_position'] 
    team_stats = team_stats.join(eligible_pos)
    team_stats = team_stats.join(selected_pos)
    return team_stats

def get_position_stats(team_stats, pos):
    pos_mask = team_stats.eligible_positions.apply(lambda x: str(pos) in x)
    return team_stats[pos_mask]

def get_weekly_totals(league, team):
    total_weeks = 17
    player_id_list = team['player_id'].tolist()
    weekly_data = pd.DataFrame(team['name'])
    #week_1_data = league.player_stats(player_id_list, req_type='week', week=1)
    #weekly_data = pd.concat([week_1_data['name'], week_1_data['total_points']], axis=1, keys=['name', '1'])
    for i in range(1, 17):
        new_week = league.player_stats(player_id_list, req_type='week', week=i)
        new_week = pd.json_normalize(new_week)
        new_week['total_points'] = pd.to_numeric(new_week['total_points'])
        new_totals = new_week['total_points'].tolist()
        weekly_data.insert(i, str(i), new_totals, True)
    return weekly_data.sort_values('name')
        




