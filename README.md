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

## Quantitative Analysis Implemented

- **Scope:**: End-to-end notebook pipeline that converts raw news headlines into daily, per-symbol sentiment measures and studies their relationship with daily stock returns.
- **Inputs:**: Primary news CSV `data/raw_analyst_ratings.csv` (requires a timestamp, headline/title, and symbol/ticker column). Optional local price CSVs at `data/{SYMBOL}.csv` per ticker; if absent the pipeline will attempt to fetch prices from `yfinance`.
- **Processing Steps:**:
  - **Date alignment:** map each headline timestamp to the trading day (headlines published at or after 16:00 are assigned to the next business day).
  - **Cleaning:** normalize and strip URLs/punctuation from headlines (`clean_headline`).
  - **Sentiment scoring:** VADER (`nltk.sentiment.vader`) is used when available; otherwise `TextBlob` is used; a lightweight keyword-based fallback is used if neither is installed.
  - **Aggregation:** compute mean daily sentiment and headline counts per `symbol` + trading day.
  - **Price & returns:** load daily price series (local CSV or `yfinance`), resample/forward-fill to business calendar, compute daily percent returns from `Adj Close`/`Close`.
  - **Merge & analysis:** join daily sentiment to daily returns, compute Pearson and Spearman correlations (per symbol), and produce scatter/regression plots.
- **Outputs:**: For each symbol with sufficient overlap the pipeline writes:
  - `outputs/sentiment_returns_{SYMBOL}.csv` — merged per-day sentiment and returns used for correlation.
  - `outputs/plot_{SYMBOL}.png` — scatter + regression plot of mean daily sentiment vs daily returns.
  - Notebook-printed summary table of correlations (`pearson` and `spearman`) and number of days used.
- **How to run (notebook):**:
  - Open `notebooks/correlation_anlysis.ipynb`, execute the top cell to load helper functions, then run:

```python
# default reads `data/raw_analyst_ratings.csv` and writes outputs to `outputs/`
run_pipeline()
```

- **Dependencies:**: recommended packages include `pandas`, `numpy`, `scipy`, `matplotlib`, `seaborn`, `nltk` (VADER lexicon), `textblob`, and `yfinance` (for price fallback). Install via:

```powershell
python -m pip install pandas numpy scipy matplotlib seaborn nltk textblob yfinance
python -c "import nltk; nltk.download('vader_lexicon')"
```

- **Notes & Caveats:**:
  - The pipeline heuristically detects timestamp/headline/symbol columns; if your CSV uses different names, update the notebook top cell or tell me the exact column names and I will adjust the parser.
  - Price downloads via `yfinance` require internet access and may be rate-limited; for reproducible runs, include local `data/{SYMBOL}.csv` files.
  - For small sample runs during development use `load_news(nrows=5000)` or enable `chunksize` to avoid loading the full CSV each iteration.
