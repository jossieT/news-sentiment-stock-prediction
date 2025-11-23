import re
import nltk
from nltk.corpus import stopwords

# Ensure stopwords are downloaded in notebook or setup
# nltk.download('stopwords')
EN_STOPWORDS = set(stopwords.words("english"))

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
    return [t for t in clean_headline(text).split() if t not in EN_STOPWORDS]
