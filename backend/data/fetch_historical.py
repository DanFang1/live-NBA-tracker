from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players
import pandas as pd


def get_player_id(name):
    matches = players.find_players_by_full_name(name)
    if not matches:
        raise ValueError(f"No player found for '{name}'")
    return matches[0]['id']


def fetch_game_log(player_name, season="2024-25"):
    player_id = get_player_id(player_name)
    log = playergamelog.PlayerGameLog(player_id=player_id, season=season)
    df = log.get_data_frames()[0]
    return df