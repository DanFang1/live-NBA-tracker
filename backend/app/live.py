import pandas as pd
import os
from nba_api.live.nba.endpoints import scoreboard, boxscore

FEATURES_PATH = os.path.join(os.path.dirname(__file__), "../data/raw/features.csv")
_features_df = pd.read_csv(FEATURES_PATH)


def get_live_game_id(player_id: int) -> str | None:
    games = scoreboard.ScoreBoard().games.get_dict()
    for game in games:
        for team in ["homeTeam", "awayTeam"]:
            for player in game[team]["players"]:
                if player["personId"] == player_id:
                    return game["gameId"]
    return None


def get_player_live_stats(player_id: int, game_id: str) -> dict | None:
    box = boxscore.BoxScore(game_id).player_stats.get_dict()
    for player in box:
        if player["personId"] == player_id:
            return {
                "pts_so_far": player["points"],
                "min_so_far": float(player["minutesCalculated"].replace("PT", "").replace("M", "")),
            }
    return None


def get_player_history(player_id: int) -> dict:
    player_rows = _features_df[_features_df["PLAYER_ID"] == player_id]
    if player_rows.empty:
        return {}
    last = player_rows.iloc[-1]
    return {
        "last5_avg_pts": last["last5_avg_pts"],
        "last5_avg_ast": last["last5_avg_ast"],
        "last5_avg_reb": last["last5_avg_reb"],
        "last5_avg_min": last["last5_avg_min"],
        "avg_pts_vs_opponent": last["avg_pts_vs_opponent"],
        "opponent_encoded": last["opponent_encoded"],
    }


def get_live_features(player_id: int) -> dict | None:
    game_id = get_live_game_id(player_id)
    if game_id is None:
        return None

    live_stats = get_player_live_stats(player_id, game_id)
    if live_stats is None:
        return None

    history = get_player_history(player_id)
    if not history:
        return None

    return {
        **history,
        "days_rest": 1,
        "is_home": 1,
    }