import pandas as pd

def get_player_stats(league, player_name):
    player_details = pd.json_normalize(league.player_details(player_name))
    player_id = player_details['player_id'].tolist()
    player_stats = league.player_stats(player_id, req_type='season', season=2025)
    player_stats = pd.json_normalize(player_stats)
    # print(player_stats._get_value(0, 'Pass TD'))
    return player_stats
