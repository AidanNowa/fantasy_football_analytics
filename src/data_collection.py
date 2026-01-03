import pandas as pd
from yahoo_fantasy_api import League, Team
import matplotlib.pyplot as plt

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
    total_weeks = 18
    if team.empty:
        return pd.DataFrame(columns=["name"])
    player_id_list = team['player_id'].tolist()
    if not player_id_list:
        return pd.DataFrame(columns=["name"])

    weekly_data = pd.DataFrame(team['name'])
    #week_1_data = league.player_stats(player_id_list, req_type='week', week=1)
    #weekly_data = pd.concat([week_1_data['name'], week_1_data['total_points']], axis=1, keys=['name', '1'])
    for i in range(1, total_weeks):
        new_week = league.player_stats(player_id_list, req_type='week', week=i)
        if not new_week:
            continue
        new_week = pd.json_normalize(new_week)
        new_week['total_points'] = pd.to_numeric(new_week['total_points'])
        new_totals = new_week['total_points'].tolist()
        weekly_data.insert(i, str(i), new_totals, True)
    return weekly_data.sort_values('name')

def calculate_margin(weekly_totals, projections, curr_week):
    '''
     weekly_totals = weekly_totals.reset_index(drop=True)
    projections_margin = pd.DataFrame(projections['name'])
    for i in range(1, curr_week+1):
        week_margin = (weekly_totals[str(i)] - projections[str(i)])
        margin = week_margin.to_list()
        projections_margin.insert(i, str(i), margin, True)
    return projections_margin        
    '''
    weekly_totals = weekly_totals.set_index("name")
    projections = projections.set_index("name")
    
    common_players = weekly_totals.index.intersection(projections.index)
    weekly_totals = weekly_totals.loc[common_players]
    projections = projections.loc[common_players]

    #only keep players that exist in weekly_totals
    projections_margin = pd.DataFrame(index=weekly_totals.index).reset_index()
    for i in range(1, curr_week + 1):
        week = str(i)
        week_margin = (weekly_totals[week] - projections.loc[weekly_totals.index, week])
        projections_margin.insert(i, week, week_margin.to_list(), True)
    return projections_margin


def create_weekly_line_graph(df, x_axis_label, y_axis_label):
    df_long = df.melt(id_vars='name', var_name=x_axis_label, value_name=y_axis_label)
    df_long[x_axis_label] = df_long[x_axis_label].astype(int)
    for name, group in df_long.groupby('name'):
        plt.plot(group[x_axis_label], group[y_axis_label], marker = 'o', label=name)
    plt.xlabel(x_axis_label)
    plt.ylabel(y_axis_label)
    plt.legend()
    plt.grid(True)
    plt.show()

def get_positional_margins(team_stats, pos, margins):
    pos_stats = get_position_stats(team_stats, pos)
    pos_names = pos_stats['name'].to_list()
    return margins[margins['name'].isin(pos_names)] 

def sum_margins(margins):
    sum_df = margins.set_index('name')
    return sum_df.sum(axis=1)

def get_weekly_longs(weekly_totals):
    weekly_totals_long = weekly_totals.melt(id_vars='name', var_name='week', value_name='points')
    weekly_totals_long['week'] = weekly_totals_long['week'].astype(int)
    return weekly_totals_long

def get_margin_weekly_longs(weekly_margins):
    weekly_margins_long = weekly_margins.melt(id_vars='name', var_name='week', value_name=    'margin')
    weekly_margins_long['week'] = weekly_margins_long['week'].astype(int)
    weekly_margins_long = weekly_margins_long.dropna(subset=["margin"])
    return weekly_margins_long

def get_weekly_longs_by_position(league, team, position) -> pd.DataFrame:
    team_stats = get_team_yearly_stats(league, team)
    pos_stats = get_position_stats(team_stats, position)
    pos_weekly = get_weekly_totals(league, pos_stats)
    return get_weekly_longs(pos_weekly)    

def get_margin_longs_by_position(league, team, position, projections) -> pd.DataFrame:
    curr_week = 17
    team_stats = get_team_yearly_stats(league, team)
    pos_stats = get_position_stats(team_stats, position)
    pos_weekly = get_weekly_totals(league, pos_stats)
    pos_margin = calculate_margin(pos_weekly, projections, curr_week)
    return get_margin_weekly_longs(pos_margin)    





