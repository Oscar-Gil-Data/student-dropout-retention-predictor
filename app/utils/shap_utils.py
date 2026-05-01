import shap
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np

_explainer_cache = {}

def get_explainer(model, model_name: str):
    if model_name not in _explainer_cache:
        _explainer_cache[model_name] = shap.TreeExplainer(model)
    return _explainer_cache[model_name]

def get_shap_values(model, model_name: str, input_df: pd.DataFrame):
    explainer = get_explainer(model, model_name)
    return explainer(input_df)

def plot_waterfall(shap_values, class_idx: int, class_name: str, max_display: int = 10):
    """Render a SHAP waterfall plot for a single prediction and class."""
    fig, ax = plt.subplots(figsize=(8, 5))
    shap.plots.waterfall(
        shap_values[0, :, class_idx],
        max_display=max_display,
        show=False
    )
    plt.title(f'Feature impact on {class_name} prediction', fontsize=11, fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig, clear_figure=True)
