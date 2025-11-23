from src.utils import Loader


def test_loader_class_basic():
    loader = Loader()
    df = loader.load(path="tests/fixtures/raw_analyst_ratings.csv")
    assert "headline" in df.columns
    assert df.shape[0] >= 1
