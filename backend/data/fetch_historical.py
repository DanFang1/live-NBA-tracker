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

    raw_dir = os.path.join(os.path.dirname(__file__), "raw")
    existing_path = os.path.join(raw_dir, "all_players_2020_2025.csv")
    output_path = os.path.join(raw_dir, "all_players_2020_2026.csv")

    existing = pd.read_csv(existing_path)
    player_ids = existing["PLAYER_ID"].unique().tolist()
    print(f"Fetching 2025-26 for {len(player_ids)} players...")

    new_data = []

    for player_id in player_ids:
        try:
            log = playergamelog.PlayerGameLog(player_id=player_id, season="2025-26")
            df = log.get_data_frames()[0]
            df["PLAYER_ID"] = player_id
            new_data.append(df)
            print(f"  Player {player_id} — {len(df)} games")
        except Exception as e:
            print(f"  Skipped {player_id}: {e}")
        time.sleep(0.6)

    new_season = pd.concat(new_data, ignore_index=True)
    combined = pd.concat([existing, new_season], ignore_index=True)
    combined.to_csv(output_path, index=False)
    print(f"Done — {len(combined)} total rows saved to {output_path}")