import subprocess
import sys
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parent.parent


def generate(tmp_path):
    subprocess.run([sys.executable, str(REPO / "datagen.py")], cwd=tmp_path, check=True)
    return (
        pd.read_csv(tmp_path / "listening_logs.csv"),
        pd.read_csv(tmp_path / "songs_metadata.csv"),
    )


def test_generated_shapes_and_columns(tmp_path):
    logs, songs = generate(tmp_path)
    assert list(logs.columns) == ["user_id", "song_id", "timestamp", "duration_sec"]
    assert list(songs.columns) == ["song_id", "title", "artist", "genre", "mood"]
    assert len(logs) == 1000 and len(songs) == 50


def test_generator_is_deterministic(tmp_path):
    first = tmp_path / "a"
    second = tmp_path / "b"
    first.mkdir()
    second.mkdir()
    logs_a, songs_a = generate(first)
    logs_b, songs_b = generate(second)
    pd.testing.assert_frame_equal(logs_a, logs_b)
    pd.testing.assert_frame_equal(songs_a, songs_b)


def test_every_log_refers_to_a_known_song_and_valid_duration(tmp_path):
    logs, songs = generate(tmp_path)
    assert set(logs["song_id"]) <= set(songs["song_id"])
    assert logs["duration_sec"].between(30, 300).all()
