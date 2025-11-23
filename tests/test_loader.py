from src.utils.loader import load_news
import os

def test_loader_basic():
    # Allow overriding test data via environment variable (useful for CI)
    env_path = os.environ.get("TEST_DATA_PATH")
    fixture_path = os.path.join("tests", "fixtures", "raw_analyst_ratings.csv")
    if env_path:
        path = env_path
    elif os.path.exists(fixture_path):
        path = fixture_path
    else:
        path = "data/raw_analyst_ratings.csv"

    assert os.path.exists(path), f"Test data not found at {path}"
    df = load_news(path)
    # check essential columns
    for col in ["headline", "date_utc", "publisher_clean", "headline_len_chars"]:
        assert col in df.columns
    # date_utc should be timezone-aware
    assert df["date_utc"].dtype == "datetime64[ns, UTC]" or df["date_utc"].dt.tz is not None
