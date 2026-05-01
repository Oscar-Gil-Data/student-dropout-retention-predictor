import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Model Performance", layout="wide")
st.title("Model Performance")
st.markdown(
    "Classification metrics and a statistically rigorous comparison of models "
    "using McNemar's test on paired predictions from the same held-out test set."
)

st.divider()

# --- Per-class metrics ---
st.subheader("Per-class classification report")
st.markdown("*Placeholder — populate after training models in notebooks/03_modeling.ipynb*")

# Example structure for when metrics are loaded
metrics_placeholder = pd.DataFrame({
    "Class":     ["Dropout", "Enrolled", "Graduate"],
    "Precision": [0.00,       0.00,        0.00],
    "Recall":    [0.00,       0.00,        0.00],
    "F1":        [0.00,       0.00,        0.00],
    "Support":   [0,          0,           0],
})
st.dataframe(metrics_placeholder, use_container_width=True)

st.divider()

# --- McNemar's test ---
st.subheader("McNemar's test — classifier comparison")
st.markdown(
    """
    Rather than comparing classifiers by accuracy alone, McNemar's test evaluates whether
    two models disagree significantly on the **same** test observations. This is the
    methodologically correct approach for paired classifier comparison — widely used in
    clinical research but rarely applied in data science portfolios.

    The test focuses only on the cases where models **disagree** (cells b and c below),
    ignoring cases where both models are correct or both are wrong.
    """
)

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("#### Contingency table")
    contingency_placeholder = pd.DataFrame(
        {
            "Model B correct": [0, 0],
            "Model B wrong":   [0, 0],
        },
        index=["Model A correct", "Model A wrong"]
    )
    st.dataframe(contingency_placeholder, use_container_width=True)
    st.caption("*Populate after running notebooks/04_mcnemar_comparison.ipynb*")

with col2:
    st.markdown("#### Test result")
    st.metric("Chi-square statistic", "—")
    st.metric("p-value", "—")
    st.markdown(
        """
        **Interpretation:** A p-value below 0.05 indicates the two models make
        significantly different errors — one is statistically preferable. A p-value
        above 0.05 means the difference in errors could be due to chance.
        """
    )

st.divider()

# --- Confusion matrix ---
st.subheader("Confusion matrix")
st.markdown("*Placeholder — populate after training*")
