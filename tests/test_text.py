from src.utils.text import clean_headline, tokenize


def test_clean_headline_basic():
    s = "I love Python! Visit http://example.com"
    cleaned = clean_headline(s)
    assert isinstance(cleaned, str)
    assert "http" not in cleaned


def test_tokenize_and_stopwords():
    toks = tokenize("I am teacher and I love teaching.")
    assert isinstance(toks, list)
    # stopword 'i' should be removed by default fallback or nltk
    assert "i" not in toks
