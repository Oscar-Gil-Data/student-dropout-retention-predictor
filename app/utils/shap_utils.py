import shap
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


def get_shap_values(model, input_df: pd.DataFrame):
    """Compute SHAP values for a single prediction row."""
    explainer = shap.TreeExplainer(model)
    shap_values = explainer(input_df)
    return shap_values


def plot_waterfall(shap_values, class_index: int = 0, max_display: int = 10):
    """
    Render a SHAP waterfall plot for a single prediction and class.
    class_index: 0 = Dropout, 1 = Enrolled, 2 = Graduate
    """
    fig, ax = plt.subplots()
    shap.plots.waterfall(shap_values[0, :, class_index], max_display=max_display, show=False)
    st.pyplot(fig, clear_figure=True)
