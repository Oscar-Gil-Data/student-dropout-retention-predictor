import streamlit as st
import os

st.header("Exploratory Data Analysis")
st.caption("Charts generated from the mart layer in notebook 01. All analysis starts from fct_enrollment_outcomes.")

BASE = os.path.join(os.path.dirname(__file__), '../..', 'data')

charts = [
    ("Class distribution",                  "eda_class_distribution.png"),
    ("Academic performance distributions",  "eda_academic_distributions.png"),
    ("Financial indicators",                "eda_financial_signals.png"),
    ("Dropout rate by course",              "eda_dropout_by_course.png"),
    ("Unit approval rate distributions",    "eda_approval_rates.png"),
    ("Feature correlation matrix",          "eda_correlation_matrix.png"),
]

for title, filename in charts:
    path = os.path.join(BASE, filename)
    if os.path.exists(path):
        st.markdown(f"#### {title}")
        st.image(path, use_container_width=True)
        st.divider()
    else:
        st.warning(f"{filename} not found -- run notebook 01 to generate EDA charts.")
