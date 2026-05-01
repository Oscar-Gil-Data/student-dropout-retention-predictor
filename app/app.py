import streamlit as st

st.set_page_config(
    page_title="Student Dropout & Retention Predictor",
    page_icon="🎓",
    layout="wide",
)

st.title("Student Dropout & Retention Predictor")
st.markdown(
    """
    An end-to-end analytics engineering and data science project built on the
    [UCI Student Dropout dataset](https://archive.ics.uci.edu/dataset/697/predict+students+dropout+and+academic+success).

    Use the sidebar to navigate between pages:
    - **Prediction** — adjust a student profile and see a live dropout risk prediction with SHAP explainability
    - **Model Performance** — confusion matrix, per-class metrics, and McNemar's test comparing classifiers
    - **EDA** — exploratory analysis of dropout patterns across courses, demographics, and academic performance
    - **About** — project architecture, dbt lineage, and methodology notes
    """
)

st.info("Select a page from the sidebar to get started.")
