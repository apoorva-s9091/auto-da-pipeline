# auto-da-pipeline

Automated end-to-end data analysis pipeline. Upload any dataset and get a full analysis report.

## Usage
```bash
pip install -r requirements.txt
python run.py --input data.csv --output reports/
```

## Pipeline
Ingestion → Validation → Profiling → Cleaning → EDA → Report