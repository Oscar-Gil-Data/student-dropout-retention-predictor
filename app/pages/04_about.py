import streamlit as st

st.header("About this project")

st.markdown("""
### Building the pipeline. Building the model.

An end-to-end analytics engineering and data science project built on the
[UCI Predict Students Dropout and Academic Success dataset](https://archive.ics.uci.edu/dataset/697/predict+students+dropout+and+academic+success).
4,424 students, 36 features, 3-class outcome: Dropout, Enrolled, Graduate.
""")

st.divider()

tab1, tab2, tab3 = st.tabs(["Architecture", "Features", "Results"])

# ── Tab 1: Architecture ───────────────────────────────────────────────
with tab1:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        #### Layer 1 -- dbt (Analytics Engineering)

        The raw flat file is normalized into a Kimball-style dimensional model
        running on DuckDB locally and BigQuery in production.

        - `stg_students` -- column renaming, type casting
        - `int_student_demographics` -- student-level demographic attributes
        - `int_program_context` -- course/attendance combinations
        - `int_economic_context` -- macroeconomic period attributes
        - `fct_enrollment_outcomes` -- student-grain fact table, 12 dbt tests passing

        Macroeconomic features (GDP, inflation, unemployment) are extracted into
        their own dimension -- they are period-level attributes shared across
        students, not student-level facts.
        """)

        st.markdown("""
        #### Layer 2 -- Python Modeling

        - Notebook 01: EDA from mart layer
        - Notebook 02: Feature engineering, train/test split, class weights
        - Notebook 03: Logistic Regression and Random Forest with per-class F1,
          ROC curves, and cross-validation
        - Notebook 04: McNemar's test for statistically rigorous model comparison
        """)

    with col2:
        st.markdown("""
        #### Tech stack

        | Layer | Tools |
        |---|---|
        | Analytics Engineering | dbt Core, DuckDB, SQL |
        | Data Platform | BigQuery (production) |
        | Modeling | Python, scikit-learn, pandas |
        | Explainability | SHAP |
        | Statistical testing | McNemar's test (statsmodels) |
        | App | Streamlit |
        | Version control | Git, GitHub |
        """)

        st.markdown("""
        #### McNemar's test

        Rather than comparing classifiers by accuracy alone, this project applies
        McNemar's test -- a paired statistical test that evaluates whether two models
        disagree significantly on the same test observations. This is the
        methodologically correct approach for paired classifier comparison, widely
        used in clinical research but rarely applied in data science portfolios.

        **Overall result:** RF is statistically superior (p=0.0042).

        **Per-class nuance:**
        - RF dominates on Dropout (p=0.0013) and Graduate (p<0.0001)
        - LR is significantly better on Enrolled (p<0.0001) -- the minority
          class most relevant to early intervention
        """)

# ── Tab 2: Features ───────────────────────────────────────────────────
with tab2:
    st.markdown("""
    #### Engineered features

    Four features were derived during preprocessing in notebook 02.
    These are not in the original UCI dataset -- they were constructed
    to capture signals identified during EDA.
    """)

    eng_df = {
        'Feature': [
            'sem1_approval_rate',
            'sem2_approval_rate',
            'combined_approval_rate',
            'units_approved_delta',
            'grade_delta',
            'financial_stress',
        ],
        'Definition': [
            'sem1_units_approved / sem1_units_enrolled',
            'sem2_units_approved / sem2_units_enrolled',
            'Mean of sem1_approval_rate and sem2_approval_rate',
            'sem2_units_approved - sem1_units_approved',
            'sem2_grade - sem1_grade',
            '1 if is_debtor=1 AND tuition_fees_up_to_date=0, else 0',
        ],
        'Rationale': [
            'Proportion of enrolled units passed -- normalizes for course load differences',
            'Same as above for semester 2',
            'Single summary of overall approval performance across both semesters',
            'Academic trajectory -- positive means improving, negative means declining',
            'Grade trajectory across semesters',
            'Interaction term capturing compounded financial risk',
        ],
        'Top feature?': ['Yes (1st)', 'Yes (2nd)', 'Yes (3rd)', 'Yes (9th)', 'No', 'No'],
    }

    import pandas as pd
    st.dataframe(pd.DataFrame(eng_df), use_container_width=True, hide_index=True)

    st.markdown("""
    Note: `sem1_approval_rate` and `sem2_approval_rate` are derived in the
    dbt mart layer (`fct_enrollment_outcomes`). The remaining four features
    are computed in notebook 02 before training.
    """)

    st.divider()

    st.markdown("""
    #### Top features by importance (Random Forest)

    The five most important features by mean decrease in impurity, all of which
    are approval-rate or grade signals from the first two semesters.
    """)

    top_features = {
        'Rank': [1, 2, 3, 4, 5],
        'Feature': [
            'combined_approval_rate',
            'sem2_approval_rate',
            'sem2_grade',
            'sem2_units_approved',
            'sem1_grade',
        ],
        'Type': [
            'Engineered',
            'Engineered (dbt mart)',
            'Raw',
            'Raw',
            'Raw',
        ],
        'Description': [
            'Average approval rate across both semesters',
            'Proportion of semester 2 units passed',
            'Average grade in semester 2 (0-20 scale)',
            'Number of semester 2 units approved',
            'Average grade in semester 1 (0-20 scale)',
        ],
    }
    st.dataframe(pd.DataFrame(top_features), use_container_width=True, hide_index=True)

    st.markdown("""
    For the full list of original UCI features and their descriptions, see the
    [UCI dataset documentation](https://archive.ics.uci.edu/dataset/697/predict+students+dropout+and+academic+success).
    """)

# ── Tab 3: Results ────────────────────────────────────────────────────
with tab3:
    st.markdown("""
    #### Model results summary
    """)

    results = {
        'Metric': [
            'Accuracy',
            'Macro F1',
            'Macro ROC AUC',
            'Dropout F1',
            'Enrolled F1',
            'Graduate F1',
            'CV macro F1 (5-fold)',
        ],
        'Logistic Regression': [
            '0.730', '0.698', '0.877',
            '0.766', '0.506', '0.822',
            '0.706 (+/- 0.012)',
        ],
        'Random Forest': [
            '0.770', '0.695', '0.888',
            '0.791', '0.436', '0.858',
            '0.694 (+/- 0.009)',
        ],
        'Winner': [
            'RF', 'LR', 'RF',
            'RF', 'LR', 'RF',
            'LR',
        ],
    }

    import pandas as pd
    st.dataframe(pd.DataFrame(results), use_container_width=True, hide_index=True)

    st.markdown("""
    #### McNemar's test conclusion

    Overall: RF makes significantly fewer errors (p=0.0042, chi-square=8.20).

    Per-class McNemar results confirm the tradeoff:

    | Class | LR only correct | RF only correct | p-value | Better model |
    |---|---|---|---|---|
    | Dropout  | 5  | 23 | 0.0013 | RF |
    | Enrolled | 48 | 5  | <0.0001 | LR |
    | Graduate | 0  | 60 | <0.0001 | RF |

    For a general-purpose classifier, choose Random Forest.
    For early intervention targeting students still enrolled, choose Logistic Regression.
    """)

st.divider()
st.markdown("""
**Oscar Gil** -- Data Scientist & Analytics Engineer

[oscargildata.com](https://oscargildata.com) · [LinkedIn](https://linkedin.com/in/oscar-gil) · [GitHub](https://github.com/Oscar-Gil-Data)
""")