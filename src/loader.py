import pandas as pd
import re
from dateutil import parser
import pytz

DATA_PATH = "data/raw_analyst_ratings.csv"

def parse_mixed_date(x):
    """Parse mixed date formats and return UTC tz-aware Timestamp or NaT."""
    if pd.isna(x):
        return pd.NaT
    s = str(x).strip()
    # If already ISO-like with timezone, pandas will handle it
    try:
        ts = pd.to_datetime(s, utc=True)
        if ts.tzinfo is None:
            # ensure tz-aware (assume New York / ET if no tz present)
            eastern = pytz.timezone("America/New_York")
            ts = eastern.localize(pd.to_datetime(s)).astimezone(pytz.UTC)
        return ts
    except Exception:
        try:
            # fallback to dateutil parse and assume America/New_York if naive
            dt = parser.parse(s)
            if dt.tzinfo is None:
                eastern = pytz.timezone("America/New_York")
                dt = eastern.localize(dt)
            return pd.to_datetime(dt).astimezone(pytz.UTC)
        except Exception:
            return pd.NaT

def extract_publisher_domain(p):
    """If publisher looks like an email, return domain; otherwise None."""
    if pd.isna(p):
        return None
    m = re.search(r'@([\w\.-]+)', str(p))
    return m.group(1).lower() if m else None

def load_news(path: str = DATA_PATH) -> pd.DataFrame:
    """Load raw news CSV and perform initial normalization."""
    df = pd.read_csv(path, dtype=str)
    # clean column names
    df.columns = [c.strip() for c in df.columns]
    # parse dates
    df["date_parsed"] = df["date"].apply(parse_mixed_date)
    df = df.dropna(subset=["date_parsed"]).copy()
    df["date_utc"] = df["date_parsed"].dt.tz_convert("UTC")
    # publisher normalization
    df["publisher_domain"] = df["publisher"].apply(extract_publisher_domain)
    df["publisher_clean"] = df.apply(
        lambda row: row["publisher_domain"]
        if pd.notna(row["publisher_domain"])
        else row["publisher"],
        axis=1,
    )
    # headline lengths
    df["headline"] = df["headline"].astype(str)
    df["headline_len_chars"] = df["headline"].str.len()
    df["headline_len_words"] = df["headline"].str.split().apply(lambda x: len(x) if isinstance(x, list) else 0)
    # normalize ticker
    if "stock" in df.columns:
        df["stock"] = df["stock"].str.strip().str.upper()
    return df