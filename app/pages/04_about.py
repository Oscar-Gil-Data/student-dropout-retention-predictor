import streamlit as st

st.set_page_config(page_title="About", layout="wide")
st.title("About this project")

st.markdown(
    """
    ## Building the pipeline. Building the model.

    This project demonstrates end-to-end ownership of an analytics engineering and data science
    workflow — from raw data normalization through dbt to a deployed interactive prediction app.

    It was built to make a production-style architecture visible using public data, mirroring
    the kind of institutional analytics work done in higher education settings.

    ---

    ## Dataset

    **UCI Predict Students' Dropout and Academic Success**
    - 4,424 students across multiple undergraduate programs at a Portuguese higher education institution
    - 36 features: academic performance, demographics, socioeconomic factors, macroeconomic indicators
    - 3-class target: Dropout, Enrolled, Graduate
    - Strong class imbalance toward one class — handled explicitly in modeling

    ---

    ## Architecture

    ### Layer 1 — dbt (Analytics Engineering)

    The raw flat file is normalized into a Kimball-style dimensional model:

    - `stg_students` — column renaming, type casting, no logic
    - `int_student_demographics` — student-level demographic and household attributes
    - `int_program_context` — course/attendance combinations with decoded labels
    - `int_economic_context` — macroeconomic period attributes extracted from student rows
    - `fct_enrollment_outcomes` — student-grain fact table with FK references and derived metrics

    Key decision: macroeconomic features (GDP, inflation, unemployment) are period-level attributes
    shared across students. Keeping them in the fact table would be semantically incorrect and
    redundant. They are extracted into `dim_economic_context`.

    ### Layer 2 — Python Modeling

    Multi-classifier pipeline with rigorous evaluation:
    - Logistic Regression (baseline)
    - Random Forest
    - Class imbalance handling (documented and justified)
    - McNemar's test for paired classifier comparison

    **On McNemar's test:** Standard model comparison using accuracy or cross-validation scores
    treats model predictions as independent. When two classifiers are evaluated on the same
    held-out test set, the predictions are paired — McNemar's test respects that structure.
    It evaluates only the cases where models disagree, which is where the meaningful signal lives.

    ### Layer 3 — Streamlit App

    - Live prediction with sidebar feature inputs
    - SHAP waterfall chart explaining each individual prediction
    - Model performance tab with McNemar contingency table and p-value
    - EDA explorer

    ---

    ## Author

    **Oscar Gil** — Data Scientist & Analytics Engineer

    - [oscargildata.com](https://oscargildata.com)
    - [LinkedIn](https://linkedin.com/in/oscar-gil)
    - [GitHub](https://github.com/Oscar-Gil-Data)
    """
)
