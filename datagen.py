# datagen.py
import pandas as pd
import random
from datetime import datetime, timedelta

# -------------------------------
# Config
# -------------------------------
random.seed(42)
num_users = 100
num_songs = 50
num_logs = 1000

user_ids = [f'user_{i}' for i in range(1, num_users+1)]
song_ids = [f'song_{i}' for i in range(1, num_songs+1)]

genres = ['Pop', 'Rock', 'Jazz', 'Classical', 'Hip-Hop']
moods = ['Happy', 'Sad', 'Energetic', 'Chill']

# Assign some users as "loyalists"
preferred_genres = {
    "user_1": "Pop",
    "user_2": "Rock",
    "user_3": "Jazz"
}

# -------------------------------
# Generate listening_logs.csv
# -------------------------------
logs = []
start_date = datetime(2025, 3, 1)
end_date = datetime(2025, 3, 28)

for _ in range(num_logs):
    user = random.choice(user_ids)
    song = random.choice(song_ids)
    timestamp = (start_date + timedelta(
        seconds=random.randint(0, int((end_date - start_date).total_seconds())))
    ).strftime('%Y-%m-%d %H:%M:%S')
    duration = random.randint(30, 300)

    logs.append([user, song, timestamp, duration])

pd.DataFrame(logs, columns=['user_id', 'song_id', 'timestamp', 'duration_sec']) \
    .to_csv('listening_logs.csv', index=False)

# -------------------------------
# Generate songs_metadata.csv
# -------------------------------
metadata = []
for song_id in song_ids:
    # If song belongs to a "loyalist" genre, make sure it exists
    if random.random() < 0.2:  # ~20% chance of being from loyalist pool
        genre = random.choice(list(preferred_genres.values()))
    else:
        genre = random.choice(genres)

    metadata.append([
        song_id,
        f'Title_{song_id}',
        f'Artist_{random.randint(1, 20)}',
        genre,
        random.choice(moods)
    ])

pd.DataFrame(metadata, columns=['song_id', 'title', 'artist', 'genre', 'mood']) \
    .to_csv('songs_metadata.csv', index=False)
