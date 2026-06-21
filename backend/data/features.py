import pandas as pd
import os


def load_data():
    path = os.path.join(os.path.dirname(__file__), "raw", "all_players_2020_2026.csv")
    df = pd.read_csv(path)
    df["GAME_DATE"] = pd.to_datetime(df["GAME_DATE"], format="mixed")
    df = df.sort_values(["PLAYER_ID", "GAME_DATE"]).reset_index(drop=True)
    return df


def add_rolling_features(df):
    df = df.copy()
    for stat in ["PTS", "AST", "REB", "MIN"]:
        df[f"last5_avg_{stat.lower()}"] = (
            df.groupby("PLAYER_ID")[stat]
            .transform(lambda x: x.shift(1).rolling(5, min_periods=1).mean())
        )
    return df


def add_game_context_features(df):
    df = df.copy()
    df["days_rest"] = (
        df.groupby("PLAYER_ID")["GAME_DATE"]
        .transform(lambda x: x.diff().dt.days.fillna(3))
    )
    df["is_home"] = df["MATCHUP"].apply(lambda x: 0 if "@" in x else 1)
    df["opponent"] = df["MATCHUP"].apply(lambda x: x.split()[-1])
    df["opponent_encoded"] = df["opponent"].astype("category").cat.codes
    return df


def add_matchup_features(df):
    df = df.copy()
    matchup_avg = (
        df.groupby(["PLAYER_ID", "opponent"])["PTS"]
        .transform(lambda x: x.shift(1).expanding().mean())
    )
    df["avg_pts_vs_opponent"] = matchup_avg
    df["avg_pts_vs_opponent"] = df["avg_pts_vs_opponent"].fillna(df["last5_avg_pts"])
    return df


def build_features(df):
    df = add_rolling_features(df)
    df = add_game_context_features(df)
    df = add_matchup_features(df)
    df = df.dropna(subset=["last5_avg_pts", "days_rest"])
    return df


if __name__ == "__main__":
    df = load_data()
    df = build_features(df)
    output_path = os.path.join(os.path.dirname(__file__), "raw", "features.csv")
    df.to_csv(output_path, index=False)
    print(f"Done — {len(df)} rows, {len(df.columns)} columns")
    print(df[["PLAYER_ID", "PTS", "last5_avg_pts", "days_rest", "is_home", "avg_pts_vs_opponent"]].head())