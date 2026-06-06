from pathlib import Path
from typing import Optional, Union
import pandas as pd
from sqlmodel import Session
from app.database import engine, create_db_and_tables
from app.models import TaxiTrip

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
            raise FileNotFoundError(f"No CSV file found in {data_dir}")
        csv_path = csv_files[0]
    print(f"Reading CSV: {csv_path}")
    for encoding in ["utf-8", "utf-8-sig", "latin1", "cp1252"]:
        try:
            return pd.read_csv(csv_path, encoding=encoding, low_memory=False)
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Could not read CSV file: {csv_path}")

def bulk_insert():
    create_db_and_tables()
    df = load_df()
    print(f"Loaded rows: {len(df)}")
    records = df.to_dict(orient="records")
    with Session(engine) as session:
        trips = [TaxiTrip(**record) for record in records]
        session.add_all(trips)
        session.commit()
    print(f"Inserted rows: {len(trips)}")

if __name__ == "__main__":

    bulk_insert()