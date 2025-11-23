# news-sentiment-stock-prediction

**One-line:** Exploring how news sentiment and technical indicators relate to daily stock price movements for predictive analytics.

## Overview

This project analyzes financial news headlines to extract sentiment and then studies correlations between sentiment and stock price movements. Work is organized notebook-first with modular helper code.

## Folder structure

- `notebooks/` — Jupyter notebooks (EDA, topic modeling, time series)
- `src/` — reusable modules (data loaders, text utils)
- `data/` — raw and processed data
- `tests/` — unit tests
- `.github/workflows/` — CI

## How to run

1. Create Python virtual environment and activate it:

# news-sentiment-stock-prediction

One-line: analyze financial news headlines to extract sentiment and relate it to stock movements.

## Overview

This repository is notebook-first with small, reusable helpers in `src/`. The current work focuses on extracting sentiment and keywords from news headlines and preparing time-series features for downstream modeling.

## Recent / Performed Tasks

- Added a small, top-of-notebook post-run callback to `notebooks/sentiment_analysis.ipynb` that prints a short completion message after each executed cell (helps visibility during long runs).
- Replaced the project `.gitignore` with a compact set of ignores for Python projects.
- Implemented a faster, vectorized `load_news` in `src/utils/loader.py` (supports chunked CSV reads and optional Parquet caching) to speed up loading large CSVs.
- Made `src/utils/text.py` robust by lazy-loading NLTK stopwords and falling back to a lightweight builtin stopword set (avoids importing `nltk`/`regex` at module import time).

## Notebook list (high level)

- `notebooks/sentiment_analysis.ipynb` — modular EDA + NLP pipeline: data loading, cleaning, descriptive stats, sentiment (TextBlob), keyword extraction (spaCy + pyTextRank), and visualizations.
- `notebooks/00_setup.ipynb` — environment checks and initial imports (recommended to run first).
- `notebooks/01_eda_descriptive.ipynb` — descriptive statistics and plotting.
- `notebooks/02_text_analysis.ipynb` — text cleaning, n-grams, basic topic extraction.
- `notebooks/03_time_series.ipynb` — hourly & daily publication analysis.

## Data layout

- Expected raw CSV: `data/raw_analyst_ratings.csv`
- The optimized loader can optionally cache a Parquet copy at `data/raw_analyst_ratings.parquet` for much faster subsequent loads.

## Quick start (Windows PowerShell)

1. Create and activate the virtual environment, then install dependencies:

```powershell
python -m venv .venv
.venv\Scripts\Activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

2. If using spaCy features, install the English model in the same environment:

```powershell
python -m spacy download en_core_web_sm
```

3. For iteration during development, load a small sample or enable chunks:

```python
from src.utils.loader import load_news
df = load_news(nrows=5000)                # quick sample
# or use chunking and/or cache_parquet=True for faster repeated runs
```

## Troubleshooting notes

- AttributeError: module 'regex' has no attribute 'compile' — this usually indicates a stray `regex.py` file shadowing the real package. If you see this, search for `regex.py` on your system (or in your Python installation) and remove/backup it; then reinstall `regex` with `pip` in the intended environment.
- spaCy model errors (e.g. `Can't find model 'en_core_web_sm'`) — ensure the model is installed into **the same Python interpreter** used by your notebook (`python -m spacy download en_core_web_sm`). Verify with `python -c \"import spacy; spacy.load('en_core_web_sm')\"`.
- Compatibility: if spaCy imports fail due to `thinc` mismatches (ImportError referencing `ParametricAttention_v2`), reinstall compatible versions (example: `pip install \"spacy==3.7.4\" \"thinc>=8.1,<8.2\"`).

## Development tips

- Use `load_news(..., nrows=1000)` or `chunksize=10000` while iterating to avoid waiting on the full CSV.
- Convert the CSV to Parquet once (the loader can write a cache) to make reloads instant.
- When running notebooks, select the `.venv` interpreter and restart the kernel after changing environment packages.

## Files changed during recent work

- `notebooks/sentiment_analysis.ipynb` — added post-run callback cell and modular pipeline.
- `src/utils/loader.py` — optimized loader with parquet caching.
- `src/utils/text.py` — lazy stopwords + cleaning utilities.
- `.gitignore` — compact Python project ignores.

If you'd like a more formal changelog or to extract the notebook callback into a reusable helper module (e.g. `src/utils/jupyter_helpers.py`), tell me and I'll add it.

---

Generated / updated in-workspace on review.
