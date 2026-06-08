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


if __name__ == "__main__":
    import os
    import time
    from nba_api.stats.endpoints import leagueleaders

    seasons = ["2020-21", "2021-22", "2022-23", "2023-24", "2024-25"]

    leaders = leagueleaders.LeagueLeaders(season="2024-25", stat_category_abbreviation="MIN")
    top_players = leaders.get_data_frames()[0].head(150)["PLAYER_ID"].tolist()

    all_data = []

    for player_id in top_players:
        for season in seasons:
            try:
                log = playergamelog.PlayerGameLog(player_id=player_id, season=season)
                df = log.get_data_frames()[0]
                df["PLAYER_ID"] = player_id
                all_data.append(df)
                print(f"Fetched player {player_id} season {season} — {len(df)} games")
            except Exception as e:
                print(f"Skipped player {player_id} season {season}: {e}")
            time.sleep(0.6)

    combined = pd.concat(all_data, ignore_index=True)
    output_path = os.path.join(os.path.dirname(__file__), "raw", "all_players_2020_2025.csv")
    combined.to_csv(output_path, index=False)
    print(f"Done — {len(combined)} rows saved")