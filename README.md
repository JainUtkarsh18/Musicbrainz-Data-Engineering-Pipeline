#  MusicBrainz Data Engineering ETL Pipeline

A reusable Python ETL pipeline for extracting, cleaning, transforming, analyzing, and exporting music metadata from the MusicBrainz API.

The project demonstrates end-to-end data engineering concepts including API data extraction, preprocessing, exploratory data analysis (EDA), visualization, and automated reporting using a modular Python architecture.

---

## Kaggle Notebook

The original notebook is available on [Kaggle](https://www.kaggle.com/code/utkarshjain76/from-musicbrainz-to-analytics-a-metadata-pipeline).
Full generated dataset is also available on [Kaggle](https://www.kaggle.com/datasets/utkarshjain76/musicbrainz-metadata-dataset).

---

##  Project Overview

This project builds a complete ETL workflow around the MusicBrainz Web Service API.

The pipeline:

- Extracts music metadata from the MusicBrainz API
- Cleans and validates the collected data
- Performs preprocessing and feature engineering
- Generates exploratory data analysis (EDA)
- Creates visualizations
- Produces summary reports
- Exports processed datasets for downstream analytics

The repository is designed as a reusable data engineering project instead of a standalone notebook.
The generated sample size can also be changed according to need.
---

##  Features

-  MusicBrainz API Integration
-  Automated ETL Pipeline
-  Data Cleaning & Validation
-  Exploratory Data Analysis (EDA)
-  Data Visualization
-  Automated Summary Reports
-  CSV & Parquet Export
-  Modular Python Architecture

---

##  ETL Workflow

```text
MusicBrainz API
        │
        ▼
Data Extraction
        │
        ▼
Data Cleaning
        │
        ▼
Transformation
        │
        ▼
EDA
        │
        ▼
Visualization
        │
        ▼
Summary Report
        │
        ▼
CSV / Parquet Export
```

---

##  Installation

Clone the repository

```bash
git clone https://github.com/<your_username>/musicbrainz-data-engineering-etl.git
```

Navigate to the project

```bash
cd musicbrainz-data-engineering-etl
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

##  Running the Project

Open the notebook

```bash
jupyter notebook notebooks/MusicBrainz_Metadata_ETL.ipynb
```

or execute the pipeline

```python
from src.pipeline import run_pipeline

run_pipeline()
```

---

##  Output

The pipeline generates:

- Cleaned datasets
- Exploratory analysis tables
- Visualizations
- Summary reports
- CSV exports
- Parquet exports

---

## Technologies Used

- Python
- Pandas
- NumPy
- Requests
- Matplotlib
- Seaborn
- Jupyter Notebook
- MusicBrainz Web Service API

---

##  Future Improvements

- Docker support
- Apache Airflow integration
- Database storage (PostgreSQL)
- Automated unit testing
- GitHub Actions CI/CD
- Data quality validation
- Incremental ETL support

---

##  License

This project is licensed under the MIT License.

---

I am open to more collaborations and recommendations on this notebook.
