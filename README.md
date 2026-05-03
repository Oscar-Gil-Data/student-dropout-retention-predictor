# Student Dropout & Retention Predictor

> **Building the pipeline. Building the model.**

An end-to-end analytics engineering and data science project predicting student dropout risk using the [UCI Predict Students' Dropout and Academic Success dataset](https://archive.ics.uci.edu/dataset/697/predict+students+dropout+and+academic+success).

This project demonstrates a full production-style architecture -- from raw data normalization through dbt to a deployed Streamlit app with live SHAP explainability.

---

## Project Architecture

```
Raw CSV (UCI)
    │
    ▼
[ Layer 1 -- dbt ]
Staging → Intermediate → Marts
(DuckDB-native normalization, dimensional modeling)
    │
    ▼
[ Layer 2 -- Python Modeling ]
EDA → Feature Engineering → Multi-classifier comparison
(McNemar's test for statistically rigorous model selection)
    │
    ▼
[ Layer 3 -- Streamlit App ]
Live prediction · SHAP waterfall · Model performance · EDA explorer
```

---

## Dataset

- **Source**: UCI Machine Learning Repository -- [Dataset #697](https://archive.ics.uci.edu/dataset/697/predict+students+dropout+and+academic+success)
- **Instances**: 4,424 students
- **Features**: 36 (academic, demographic, socioeconomic, macroeconomic)
- **Target**: 3-class classification -- `Dropout`, `Enrolled`, `Graduate`
- **License**: CC BY 4.0

> The raw CSV is not committed to this repo. Download it from the UCI link above and place it at `data/raw/data.csv`.

---

## Layer 1 -- dbt (Analytics Engineering)

The flat UCI source file is normalized into a dimensional model following Kimball methodology.

**Model lineage:**

```
stg_students
    │
    ├── int_student_demographics
    ├── int_program_context
    └── int_economic_context
            │
            ▼
    dim_student
    dim_program
    dim_economic_context
    fct_enrollment_outcomes
```

**Key modeling decisions:**
- Macroeconomic features (GDP, inflation, unemployment) extracted into `dim_economic_context` -- shared across students enrolled in the same period, not student-level attributes
- Program and attendance mode extracted into `dim_program` -- separates course-level facts from student-level facts
- `fct_enrollment_outcomes` is at student grain with foreign keys to all dimensions and the target outcome

> dbt models in this repo are written for DuckDB SQL dialect and run locally without cloud infrastructure. The dimensional model is designed to be portable to BigQuery for production deployment. See `dbt/profiles.yml.example` to connect either adapter.

---

## Layer 2 -- Python Modeling

Notebooks are numbered and meant to be run in sequence:

| Notebook | Description |
|---|---|
| `01_eda.ipynb` | Exploratory data analysis -- class imbalance, feature distributions, correlation |
| `02_feature_engineering.ipynb` | Feature selection, encoding, class imbalance handling |
| `03_modeling.ipynb` | Multi-classifier training -- Logistic Regression, Random Forest, others |
| `04_mcnemar_comparison.ipynb` | Statistically rigorous model comparison using McNemar's test |

**On McNemar's test:** Rather than comparing classifiers by accuracy alone, this project applies McNemar's test -- a paired statistical test that evaluates whether two models disagree significantly on the *same* test observations. This is the methodologically correct approach for paired classifier comparison, widely used in clinical research but rarely seen in data science portfolios.

---

## Layer 3 -- Streamlit App

The deployed app provides an interactive interface for exploring predictions and model behavior.

**Pages:**
- **Prediction** -- Adjust student profile features via sidebar sliders/toggles, see live class probabilities and a SHAP waterfall chart explaining that specific prediction
- **Model Performance** -- Confusion matrix, per-class precision/recall/F1, ROC curves, McNemar contingency table
- **EDA** -- Dropout rate by course, semester performance distributions, feature correlation heatmap
- **About** -- Project narrative, dbt architecture, data lineage

**Run locally:**
```bash
pip install -r requirements.txt
streamlit run app/app.py
```

---

## Setup

```bash
git clone https://github.com/Oscar-Gil-Data/student-dropout-retention-predictor.git
cd student-dropout-retention-predictor
pip install -r requirements.txt
```

Download the dataset:
```bash
# Place the UCI data.csv at:
data/raw/data.csv
```

---

## Tech Stack

| Layer | Tools |
|---|---|
| Analytics Engineering | dbt (DuckDB dialect), SQL |
| Data Platform | DuckDB (local); designed for BigQuery in production |
| Modeling | Python, scikit-learn, pandas, NumPy |
| Explainability | SHAP |
| Statistical Testing | McNemar's test (statsmodels) |
| App | Streamlit |
| Version Control | Git, GitHub |

---

## Author

**Oscar Gil** -- Data Scientist & Analytics Engineer  
[oscargildata.com](https://oscargildata.com) · [LinkedIn](https://linkedin.com/in/oscar-gil)  

*Part of a portfolio demonstrating end-to-end pipeline and modeling ownership in the education analytics domain.*
