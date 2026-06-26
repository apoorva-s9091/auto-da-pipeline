# Auto-DA-Pipeline

An automated end-to-end data analysis pipeline. Upload any dataset and get a full analysis report with a single command.

## Features
- Auto data ingestion (CSV, Excel, JSON)
- Schema validation and data profiling
- Interactive data cleaning (nulls, outliers, encoding)
- Comprehensive EDA with 10+ chart types
- AI-powered custom analysis via Gemini
- HTML/PDF report generation

## Setup
```bash
git clone https://github.com/apoorva-s9091/auto-da-pipeline
cd auto-da-pipeline
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Usage
```bash
python run.py --input data.csv --output reports/
```

## Pipeline Stages
1. Ingestion — load CSV/Excel/JSON
2. Validation — schema and null checks
3. Profiling — shape, dtypes, duplicates
4. Cleaning — interactive null, outlier, encoding handling
5. EDA — distributions, correlations, boxplots, pairplots and more
6. AI Analysis — custom analysis via Gemini API
7. Report — full HTML/PDF report



## Status
🚧 In Progress
