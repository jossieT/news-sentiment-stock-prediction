import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CSV = PROJECT_ROOT / "data" / "raw_analyst_ratings.csv"
DEFAULT_PARQUET = PROJECT_ROOT / "data" / "raw_analyst_ratings.parquet"

def _resolve_path(p):
    if p is None:
        return DEFAULT_CSV
    p = Path(p)
    return p if p.is_absolute() else (PROJECT_ROOT / p).resolve()

def load_news(path: str | None = None,
              usecols: list | None = None,
              nrows: int | None = None,
              chunksize: int | None = None,
              cache_parquet: bool = True) -> pd.DataFrame:
    """
    Fast loader:
    - reads CSV with pandas (vectorized parsing)
    - supports chunksize for low-memory streaming
    - optional parquet cache for instant reloads
    """
    csv_path = _resolve_path(path)
    parquet_path = DEFAULT_PARQUET

    # use parquet cache when available and requested
    if cache_parquet and parquet_path.exists():
        return pd.read_parquet(parquet_path)

    read_args = dict(dtype=str, usecols=usecols, low_memory=False)

    if chunksize:
        parts = []
        for chunk in pd.read_csv(csv_path, chunksize=chunksize, **read_args):
            if "date" in chunk.columns:
                chunk["date_parsed"] = pd.to_datetime(chunk["date"], errors="coerce", infer_datetime_format=True, utc=True)
            # minimal processing: headline lengths and publisher normalization can be done later
            if "headline" in chunk.columns:
                chunk["headline"] = chunk["headline"].fillna("").astype(str)
                chunk["headline_len_chars"] = chunk["headline"].str.len()
                chunk["headline_len_words"] = chunk["headline"].str.split().str.len()
            parts.append(chunk)
            if nrows and sum(p.shape[0] for p in parts) >= nrows:
                break
        df = pd.concat(parts, ignore_index=True)
        if nrows:
            df = df.iloc[:nrows]
    else:
        df = pd.read_csv(csv_path, nrows=nrows, **read_args)
        if "date" in df.columns:
            df["date_parsed"] = pd.to_datetime(df["date"], errors="coerce", infer_datetime_format=True, utc=True)
        if "headline" in df.columns:
            df["headline"] = df["headline"].fillna("").astype(str)
            df["headline_len_chars"] = df["headline"].str.len()
            df["headline_len_words"] = df["headline"].str.split().str.len()

    # write parquet cache for future runs (fast)
    try:
        if cache_parquet:
            df.to_parquet(parquet_path, index=False)
    except Exception:
        pass

    return df