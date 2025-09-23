# Music Streaming Analysis Using Spark Structured APIs

## Overview

This project analyzes **music listener behavior** using Apache Spark Structured APIs.
We process two datasets (listening logs + song metadata) to extract insights such as:

* Favorite genres per user
* Average listen time per song
* Genre loyalty scores
* Night owl user detection

The project was completed as part of **ITCS 6190/8190 – Cloud Computing for Data Analysis (Fall 2025)**.

---

## Dataset Description

Datasets are generated using `datagen.py`:

1. **listening\_logs.csv**

   * `user_id` → Unique ID of the user
   * `song_id` → Unique ID of the song
   * `timestamp` → Date & time the song was played
   * `duration_sec` → Duration in seconds

2. **songs\_metadata.csv**

   * `song_id` → Unique ID of the song
   * `title` → Song title
   * `artist` → Artist name
   * `genre` → Song genre (Pop, Rock, Jazz, Classical, Hip-Hop)
   * `mood` → Mood of the song (Happy, Sad, Energetic, Chill)

Each dataset contains **at least 100 records**.

---

## Repository Structure

```
HandsOn6/
│── datagen.py          # Generates input datasets
│── main.py             # Spark analysis tasks
│── README.md           # Documentation
│── output/             # Results folder
```

---

## Output Directory Structure

Results are saved into structured subfolders:

```
output/
 ├── user_favorite_genres/
 ├── avg_listen_time_per_song/
 ├── genre_loyalty_scores/
 └── night_owl_users/
```

---

## Tasks and Outputs

### Task 1: User Favorite Genre

**Description:** Identify the most frequently played genre for each user.

**Output Folder:** `output/user_favorite_genres/`

**Results:**

```
+--------+---------+-----+
|user_id | genre   |count|
+--------+---------+-----+
|user_1  | Rock    |    3|
|user_10 | Rock    |    3|
|user_100| Rock    |    3|
|user_11 | Classical|   4|
|user_12 | Pop     |    7|
|user_13 | Hip-Hop |    4|
|user_14 | Rock    |    5|
|user_15 | Pop     |    4|
|user_16 | Pop     |    2|
|user_17 | Hip-Hop |    5|
... (total 100 users)
```

---

### Task 2: Average Listen Time per Song

**Description:** Compute the average duration (in seconds) that each song was played.

**Output Folder:** `output/avg_listen_time_per_song/`

**Results:**

```
+--------+-------------+--------+-----------------+
|song_id | title       | artist | avg_duration_sec|
+--------+-------------+--------+-----------------+
|song_29 | Title_song_29|Artist_20|          182.25|
|song_21 | Title_song_21|Artist_6 |          160.0 |
|song_37 | Title_song_37|Artist_18|188.590909090909|
|song_30 | Title_song_30|Artist_16|          171.625|
|song_12 | Title_song_12|Artist_13|166.222222222222|
|song_22 | Title_song_22|Artist_7 |158.789473684210|
|song_17 | Title_song_17|Artist_1 |          163.0 |
|song_33 | Title_song_33|Artist_2 |158.882352941176|
|song_15 | Title_song_15|Artist_12|146.727272727272|
|song_2  | Title_song_2 |Artist_13|178.823529411764|
... (50 rows total)
```

---

### Task 3: Genre Loyalty Scores (>0.8)

**Description:** Calculate the proportion of plays in each user’s favorite genre. Keep only users with loyalty > 0.8.

**Output Folder:** `output/genre_loyalty_scores/`

**Results:**

```
+--------+-----+---------------+-----------+-------------+
|user_id |genre|fav_genre_count|total_plays|loyalty_score|
+--------+-----+---------------+-----------+-------------+
|user_24 |Jazz |              5|          6|   0.83333333|
```

---

### Task 4: Night Owl Users (12 AM – 5 AM)

**Description:** Extract users who frequently listen to songs between midnight and 5 AM.

**Output Folder:** `output/night_owl_users/`

**Results:**

```
+--------+
|user_id |
+--------+
|user_58 |
|user_94 |
|user_14 |
|user_56 |
|user_22 |
|user_68 |
|user_86 |
|user_97 |
|user_65 |
|user_47 |
... (85 users in total)
```

---

## Execution Instructions

### *1. Prerequisites*

Before running, ensure the following are installed:

1. **Python 3.x**

   ```bash
   python3 --version
   ```
2. **PySpark**

   ```bash
   pip install pyspark pandas
   ```
3. **Apache Spark** (optional if running via PySpark in Codespaces)

   ```bash
   spark-submit --version
   ```

---

### *2. Running the Analysis Tasks*

#### Running in Codespaces or Locally

1. **Generate Input Data**

   ```bash
   python3 datagen.py
   ```

2. **Run Spark Analysis**

   ```bash
   python3 main.py
   ```

   or (if Spark is installed locally):

   ```bash
   spark-submit main.py
   ```

3. **Verify Outputs**

   ```bash
   ls output/
   ```

---

## Errors and Resolutions

| Error                                                            | Cause                            | Resolution                             |
| ---------------------------------------------------------------- | -------------------------------- | ---------------------------------------|
| `ModuleNotFoundError: No module named 'pyspark'`                 | PySpark not installed            | Run `pip install pyspark pandas`       |
| `Could not find a version that satisfies the requirement Python` | Wrong entry in Requirements file | Replace with `pyspark` and `pandas`    |
| Empty Task 3 results                                             | Random dataset not biased        | Updated `datagen.py` to assign loyal genres to some users |

