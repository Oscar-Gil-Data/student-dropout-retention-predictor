import shap
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

_explainer_cache = {}

def get_explainer(model, model_name: str, X_background: pd.DataFrame = None):
    if model_name not in _explainer_cache:
        if isinstance(model, RandomForestClassifier):
            _explainer_cache[model_name] = shap.TreeExplainer(model)
        elif isinstance(model, LogisticRegression):
            # LinearExplainer requires a background dataset for masking
            background = shap.maskers.Independent(X_background, max_samples=100)
            _explainer_cache[model_name] = shap.LinearExplainer(model, background)
        else:
            # Fallback for any other model type
            background = shap.maskers.Independent(X_background, max_samples=100)
            _explainer_cache[model_name] = shap.Explainer(model, background)
    return _explainer_cache[model_name]

def get_shap_values(model, model_name: str, input_df: pd.DataFrame, X_background: pd.DataFrame = None):
    explainer = get_explainer(model, model_name, X_background)
    return explainer(input_df)

def plot_waterfall(shap_values, class_idx: int, class_name: str, max_display: int = 10):
    """Render a SHAP waterfall plot for a single prediction and class."""
    fig, ax = plt.subplots(figsize=(8, 5))

    # shap_values shape differs between TreeExplainer and LinearExplainer
    # TreeExplainer: (n_samples, n_features, n_classes)
    # LinearExplainer: (n_samples, n_features) -- one set of values, not per-class
    sv = shap_values
    if hasattr(sv, 'values') and sv.values.ndim == 3:
        # Tree model -- per-class SHAP values
        shap.plots.waterfall(sv[0, :, class_idx], max_display=max_display, show=False)
    else:
        # Linear model -- single set of values
        shap.plots.waterfall(sv[0], max_display=max_display, show=False)

    plt.title(f'Feature impact on {class_name} prediction', fontsize=11, fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig, clear_figure=True)