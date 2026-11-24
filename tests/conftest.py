import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="session")
def job_output(tmp_path_factory):
    """Run main.py once on the committed CSVs, inside a temp directory.

    main.py reads and writes paths relative to its working directory, so the
    repo's own output/ folder is never touched. Returns the temp directory.
    """
    work = tmp_path_factory.mktemp("music_job")
    for name in ("main.py", "listening_logs.csv", "songs_metadata.csv"):
        shutil.copy(REPO / name, work / name)
    env = {**os.environ, "PYSPARK_PYTHON": sys.executable}
    result = subprocess.run(
        [sys.executable, "main.py"], cwd=work, env=env,
        capture_output=True, text=True, timeout=600,
    )
    assert result.returncode == 0, f"main.py failed:\n{result.stderr[-3000:]}"
    return work
