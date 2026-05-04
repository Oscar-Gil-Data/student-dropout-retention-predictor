# Student Dropout & Retention Predictor

An end-to-end analytics engineering and data science project built on the [UCI Predict Students' Dropout and Academic Success dataset](https://archive.ics.uci.edu/dataset/697/predict+students+dropout+and+academic+success). 4,424 students · 36 features · 3-class outcome: **Dropout**, **Enrolled**, **Graduate**.

**Live app: [oscar-gil-portfolio.onrender.com/sdp-prediction](https://oscar-gil-portfolio.onrender.com/sdp-prediction)**

---

## Architecture

This project is structured in two layers: an analytics engineering layer built with dbt and a machine learning layer built in Python.

### Layer 1 — Analytics Engineering (dbt + DuckDB)

The raw flat file is normalized into a Kimball-style dimensional model running on DuckDB locally and BigQuery in production.

| Model | Description |
|---|---|
| `stg_students` | Column renaming, type casting, null handling |
| `int_student_demographics` | Student-level demographic attributes |
| `int_program_context` | Course and attendance type combinations |
| `int_economic_context` | Macroeconomic period attributes (GDP, inflation, unemployment) |
| `fct_enrollment_outcomes` | Student-grain fact table, 12 dbt tests passing |

Macroeconomic features are extracted into their own intermediate model. They are period-level attributes shared across students, not student-level facts — a grain design decision that reflects standard dimensional modeling practice.

### Layer 2 — Python Modeling

| Notebook | Description |
|---|---|
| `01_eda.ipynb` | Exploratory data analysis from the mart layer |
| `02_feature_engineering.ipynb` | Feature engineering, train/test split, class weights |
| `03_modeling.ipynb` | Logistic Regression and Random Forest with per-class F1, ROC curves, cross-validation |
| `04_model_comparison.ipynb` | McNemar's test for statistically rigorous model comparison |

---

## Tech Stack

| Layer | Tools |
|---|---|
| Analytics Engineering | dbt Core, DuckDB, SQL |
| Data Platform | BigQuery (production) |
| Modeling | Python, scikit-learn, pandas |
| Explainability | SHAP |
| Statistical Testing | McNemar's test (statsmodels) |
| App | Streamlit |
| Version Control | Git, GitHub |

---

## Feature Engineering

Four features were derived during preprocessing in notebook 02. These are not in the original UCI dataset — they were constructed to capture signals identified during EDA.

| Feature | Definition | Rationale |
|---|---|---|
| `sem1_approval_rate` | `sem1_units_approved / sem1_units_enrolled` | Proportion of enrolled units passed — normalizes for course load differences |
| `sem2_approval_rate` | `sem2_units_approved / sem2_units_enrolled` | Same as above for semester 2 |
| `combined_approval_rate` | Mean of sem1 and sem2 approval rates | Single summary of overall approval performance |
| `units_approved_delta` | `sem2_units_approved - sem1_units_approved` | Academic trajectory: positive means improving |
| `grade_delta` | `sem2_grade - sem1_grade` | Grade trajectory across semesters |
| `financial_stress` | `1 if is_debtor=1 AND tuition_fees_up_to_date=0` | Interaction term capturing compounded financial risk |

`sem1_approval_rate` and `sem2_approval_rate` are derived in the dbt mart layer (`fct_enrollment_outcomes`). The remaining four features are computed in notebook 02 before training.

### Top Features by Importance (Random Forest)

| Rank | Feature | Type |
|---|---|---|
| 1 | `combined_approval_rate` | Engineered |
| 2 | `sem2_approval_rate` | Engineered (dbt mart) |
| 3 | `sem2_grade` | Raw |
| 4 | `sem2_units_approved` | Raw |
| 5 | `sem1_grade` | Raw |

---

## Model Results

### Performance Summary

| Metric | Logistic Regression | Random Forest |
|---|---|---|
| Accuracy | 0.730 | 0.770 |
| Macro F1 | 0.698 | 0.695 |
| Macro ROC AUC | 0.877 | 0.888 |
| Dropout F1 | 0.766 | 0.791 |
| Enrolled F1 | **0.506** | 0.436 |
| Graduate F1 | 0.822 | **0.858** |
| CV Macro F1 (5-fold) | 0.706 ± 0.012 | 0.694 ± 0.009 |

### McNemar's Test

Rather than comparing classifiers by accuracy alone, this project applies McNemar's test — a paired statistical test that evaluates whether two models disagree significantly on the same test observations. This is the methodologically correct approach for paired classifier comparison, widely used in clinical research but rarely applied in data science portfolios.

**Overall result:** Random Forest makes significantly fewer errors (p=0.0042, χ²=8.20).

**Per-class results:**

| Class | LR only correct | RF only correct | p-value | Better model |
|---|---|---|---|---|
| Dropout | 5 | 23 | 0.0013 | RF |
| Enrolled | 48 | 5 | <0.0001 | **LR** |
| Graduate | 0 | 60 | <0.0001 | RF |

**Conclusion:** For a general-purpose classifier, choose Random Forest. For early intervention targeting students still enrolled, choose Logistic Regression. Model selection should be use-case driven.

---

## Project Structure

```
student-dropout-retention-predictor/
├── app/
│   ├── app.py                  # Streamlit navigation shell
│   ├── pages/
│   │   └── sdp_prediction.py   # Prediction page
│   └── utils/
│       ├── sdp_predict.py      # Model loading and prediction utilities
│       └── sdp_shap_utils.py   # SHAP explainability utilities
├── dbt/
│   ├── models/
│   │   ├── staging/
│   │   ├── intermediate/
│   │   └── marts/
│   └── tests/
├── data/
│   └── processed/              # Parquet artifacts (train/test splits, predictions)
├── models/
│   └── artifacts/              # Serialized model files (.pkl)
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_modeling.ipynb
│   └── 04_model_comparison.ipynb
├── requirements.txt            # App-only dependencies for Render
└── requirements-dev.txt        # Full pipeline environment
```

---

## Running Locally

**App only:**
```bash
pip install -r requirements.txt
streamlit run app/app.py
```

**Full pipeline:**
```bash
pip install -r requirements-dev.txt
dbt run          # runs the dbt models
dbt test         # runs 12 dbt tests
# then run notebooks in order
```

---

## Dataset

[UCI Predict Students' Dropout and Academic Success](https://archive.ics.uci.edu/dataset/697/predict+students+dropout+and+academic+success): 4,424 students from a Portuguese higher education institution. Features include demographics, socioeconomic indicators, macroeconomic context, and first and second semester academic performance.

---

## Author

**Oscar Gil** — Data Scientist & Analytics Engineer

[oscargildata.com](https://oscargildata.com) · [LinkedIn](https://linkedin.com/in/oscar-gil) · [GitHub](https://github.com/Oscar-Gil-Data)