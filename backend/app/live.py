import pandas as pd
import os
from nba_api.live.nba.endpoints import scoreboard, boxscore

FEATURES_PATH = os.path.join(os.path.dirname(__file__), "../data/raw/features.csv")
_features_df = pd.read_csv(FEATURES_PATH)

