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
```bash
python -m venv .venv
source .venv/bin/activate   # mac/linux
# .venv\Scripts\activate    # windows
pip install -r requirements.txt