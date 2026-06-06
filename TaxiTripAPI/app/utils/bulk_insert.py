from pathlib import Path
from typing import Optional, Union

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data" / "raw"


def load_df(
    data_dir: Union[str, Path] = DATA_DIR,
    filename: Optional[str] = None,
) -> pd.DataFrame:
    data_dir = Path(data_dir)

    if not data_dir.exists():
        raise FileNotFoundError(f"Data directory not found: {data_dir}")

    if filename:
        csv_path = data_dir / filename
    else:
        csv_files = sorted(data_dir.glob("*.csv"))

        if not csv_files:
            raise FileNotFoundError(
                f"No CSV file found in {data_dir}. "
                "Run scripts/download_data.py or place the CSV under data/raw."
            )

        csv_path = csv_files[0]

    if csv_path.suffix != ".csv":
        raise ValueError(f"Expected CSV file, got: {csv_path.name}")

    for encoding in ["utf-8", "utf-8-sig", "latin1", "cp1252"]:
        try:
            return pd.read_csv(csv_path, encoding=encoding, low_memory=False)
        except UnicodeDecodeError:
            continue

    raise ValueError(f"Could not read CSV file: {csv_path}")
