from src.loader import load_news
import os

def test_loader_basic():
    path = "data/raw_analyst_ratings.csv"
    assert os.path.exists(path), "Test data not found at data/raw_analyst_ratings.csv"
    df = load_news(path)
    # check essential columns
    for col in ["headline", "date_utc", "publisher_clean", "headline_len_chars"]:
        assert col in df.columns
    # date_utc should be timezone-aware
    assert df["date_utc"].dtype == "datetime64[ns, UTC]" or df["date_utc"].dt.tz is not None
