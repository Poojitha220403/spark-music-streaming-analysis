"""Run the real PySpark job (main.py) and compare each output with an
independent pandas calculation on the same input files."""
import glob
from pathlib import Path

import pandas as pd
import pytest

REPO = Path(__file__).resolve().parent.parent


def read_output(work, folder, names):
    files = sorted(glob.glob(str(work / "output" / folder / "part-*.csv")))
    if not files:
        return pd.DataFrame(columns=names)
    frames = [pd.read_csv(f, header=None, names=names) for f in files if Path(f).stat().st_size]
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(columns=names)


@pytest.fixture(scope="module")
def joined():
    logs = pd.read_csv(REPO / "listening_logs.csv")
    songs = pd.read_csv(REPO / "songs_metadata.csv")
    return logs.merge(songs, on="song_id", how="inner")


def test_all_four_outputs_are_written(job_output):
    for folder in ("user_favorite_genres", "avg_listen_time_per_song",
                   "genre_loyalty_scores", "night_owl_users"):
        assert glob.glob(str(job_output / "output" / folder / "part-*.csv")), folder


def test_favorite_genre_count_is_each_users_maximum(job_output, joined):
    out = read_output(job_output, "user_favorite_genres", ["user_id", "genre", "count"])
    counts = joined.groupby(["user_id", "genre"]).size().reset_index(name="n")
    expected_max = counts.groupby("user_id")["n"].max()
    assert len(out) == joined["user_id"].nunique()
    assert out["user_id"].is_unique
    # ties can legitimately pick either genre, so compare the winning count
    for row in out.itertuples():
        assert row.count == expected_max[row.user_id]
        assert counts[(counts.user_id == row.user_id) & (counts.genre == row.genre)]["n"].iloc[0] == row.count


def test_average_listen_time_per_song(job_output, joined):
    out = read_output(job_output, "avg_listen_time_per_song",
                      ["song_id", "title", "artist", "avg_duration_sec"]).set_index("song_id")
    expected = joined.groupby("song_id")["duration_sec"].mean()
    assert set(out.index) == set(expected.index)
    for song_id, value in expected.items():
        assert out.loc[song_id, "avg_duration_sec"] == pytest.approx(value)


def test_loyalty_scores_are_above_half_and_correct(job_output, joined):
    out = read_output(job_output, "genre_loyalty_scores",
                      ["user_id", "genre", "fav_genre_count", "total_plays", "loyalty_score"])
    totals = joined.groupby("user_id").size()
    counts = joined.groupby(["user_id", "genre"]).size()
    best_share = (counts.groupby("user_id").max() / totals)
    expected_users = set(best_share[best_share > 0.5].index)
    assert set(out["user_id"]) == expected_users
    assert (out["loyalty_score"] > 0.5).all()
    for row in out.itertuples():
        assert row.total_plays == totals[row.user_id]
        assert row.loyalty_score == pytest.approx(row.fav_genre_count / row.total_plays)


def test_night_owls_are_users_with_a_play_between_midnight_and_5am(job_output, joined):
    out = read_output(job_output, "night_owl_users", ["user_id"])
    hours = pd.to_datetime(joined["timestamp"]).dt.hour
    expected = set(joined.loc[hours < 5, "user_id"])
    assert set(out["user_id"]) == expected
    assert out["user_id"].is_unique
