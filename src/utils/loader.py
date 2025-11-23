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
    import pandas as pd
    from pathlib import Path
    from typing import Optional, List

    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    DEFAULT_CSV = PROJECT_ROOT / "data" / "raw_analyst_ratings.csv"
    DEFAULT_PARQUET = PROJECT_ROOT / "data" / "raw_analyst_ratings.parquet"


    class Loader:
        """Object-oriented loader for news CSVs.

        Provides a stable API and keeps the existing `load_news` function for
        backwards compatibility.
        """

        def __init__(self, project_root: Optional[Path] = None, cache_parquet: bool = True):
            self.project_root = Path(project_root) if project_root is not None else PROJECT_ROOT
            self.cache_parquet = cache_parquet

        def _resolve_path(self, p: Optional[str]) -> Path:
            if p is None:
                return DEFAULT_CSV
            p = Path(p)
            return p if p.is_absolute() else (self.project_root / p).resolve()

        def load(
            self,
            path: Optional[str] = None,
            usecols: Optional[List[str]] = None,
            nrows: Optional[int] = None,
            chunksize: Optional[int] = None,
        ) -> pd.DataFrame:
            """Load data with the same behavior as the previous `load_news`.

            - path: file path relative to project root or absolute.
            - usecols / nrows / chunksize: forwarded to pandas.read_csv.
            """
            csv_path = self._resolve_path(path)
            parquet_path = DEFAULT_PARQUET

            if self.cache_parquet and parquet_path.exists():
                return pd.read_parquet(parquet_path)

            read_args = dict(dtype=str, usecols=usecols, low_memory=False)

            if chunksize:
                parts = []
                for chunk in pd.read_csv(csv_path, chunksize=chunksize, **read_args):
                    if "date" in chunk.columns:
                        chunk["date_parsed"] = pd.to_datetime(
                            chunk["date"], errors="coerce", infer_datetime_format=True, utc=True
                        )
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

            try:
                if self.cache_parquet:
                    df.to_parquet(parquet_path, index=False)
            except Exception:
                pass

            # Normalization for publisher fields to mirror previous behavior
            if "publisher" in df.columns:
                df["publisher_clean"] = df["publisher"].astype(str)
            else:
                df["publisher_clean"] = None

            # Ensure date_utc column exists (may be added later in pipeline)
            if "date_parsed" in df.columns:
                try:
                    df["date_utc"] = pd.to_datetime(df["date_parsed"]).dt.tz_convert("UTC")
                except Exception:
                    df["date_utc"] = pd.to_datetime(df["date_parsed"], errors="coerce")
            else:
                df["date_utc"] = pd.NaT

            return df


    def load_news(path: Optional[str] = None, **kwargs) -> pd.DataFrame:
        """Compatibility wrapper: use the Loader class under the hood."""
        loader = Loader()
        return loader.load(path=path, **kwargs)