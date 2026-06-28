import json
import logging
from app.live import get_live_features
from app.predictor import predict_with_interval
from nba_api.stats.endpoints import scoreboardv2
from datetime import date


logger = logging.getLogger(__name__)


def fetch_and_cache_all_live(redis_client):
    try:
        board = scoreboardv2.ScoreboardV2(game_date=date.today(), timeout=60)
        game_header = board.game_header.get_data_frame()
    except Exception as e:
        logger.warning(f"Scoreboard fetch failed: {e}")
        return

    live_game_ids = game_header[
        game_header["GAME_STATUS_ID"] == 2
    ]["GAME_ID"].tolist()

    if not live_game_ids:
        return
    
    from nba_api.stats.endpoints import boxscoretraditionalv2

    player_ids_in_live_games = set()
    for game_id in live_game_ids:
        try:
            box = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id, timeout=60)
            df = box.player_stats.get_data_frame()
            player_ids_in_live_games.update(df["PLAYER_ID"].tolist())
        except Exception as e:
            logger.warning(f"Box score fetch failed for {game_id}: {e}")

    for player_id in player_ids_in_live_games:
        try:
            features = get_live_features(player_id)
            if features is None:
                continue
            result = predict_with_interval(features)
            payload = json.dumps({"player_id": player_id, **result})
            redis_client.set(f"live:{player_id}", payload, ex=90)
        except Exception as e:
            logger.warning(f"Failed to cache player {player_id}: {e}")

