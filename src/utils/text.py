import re

# Lightweight fallback stopwords (used if nltk stopwords can't be loaded)
FALLBACK_STOPWORDS = {
    "a","an","the","and","or","if","in","on","at","to","for","of","is","are","was","were",
    "it","this","that","these","those","i","you","he","she","we","they","them","my","your",
    "our","their","as","by","with","from","be","have","has","had"
}

_en_stopwords = None

def _get_stopwords():
    global _en_stopwords
    if _en_stopwords is not None:
        return _en_stopwords
    try:
        # Lazy import so top-level import won't pull in nltk (which may be shadowed)
        import importlib
        corpus = importlib.import_module("nltk.corpus")
        _en_stopwords = set(corpus.stopwords.words("english"))
    except Exception:
        _en_stopwords = FALLBACK_STOPWORDS
    return _en_stopwords

def clean_headline(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = text.lower()
    # remove urls
    text = re.sub(r"http\S+", "", text)
    # remove non-alphanumeric (keep spaces)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    # collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text

def tokenize(text: str):
    stopwords = _get_stopwords()
    return [t for t in clean_headline(text).split() if t not in stopwords]
