from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players
import pandas as pd

def get_player_id(name):
    matches = players.find_players_by_full_name(name)
    if not matches:
        raise ValueError(f"No player found for '{name}'")
    return matches[0]['id']