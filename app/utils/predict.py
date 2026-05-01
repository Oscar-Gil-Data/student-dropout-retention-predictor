import pandas as pd
import joblib
import json
import os

ARTIFACTS_DIR = os.path.join(os.path.dirname(__file__), '../../models/artifacts')
META_PATH     = os.path.join(os.path.dirname(__file__), '../../data/processed/meta.json')

_model_cache = {}

def load_meta():
    with open(META_PATH) as f:
        return json.load(f)

def load_model(model_name: str):
    if model_name not in _model_cache:
        name_map = {
            'Random Forest':       'random_forest.pkl',
            'Logistic Regression': 'logistic_regression.pkl',
        }
        path = os.path.join(ARTIFACTS_DIR, name_map[model_name])
        _model_cache[model_name] = joblib.load(path)
    return _model_cache[model_name]

def build_input_df(feature_values: dict, meta: dict) -> pd.DataFrame:
    """Build a single-row DataFrame in the exact column order the model expects."""
    row = {col: feature_values.get(col, 0) for col in meta['feature_cols']}
    return pd.DataFrame([row])

def predict(model, input_df: pd.DataFrame, classes: list) -> dict:
    proba = model.predict_proba(input_df)[0]
    pred_idx = proba.argmax()
    return {
        'prediction': classes[pred_idx],
        'probabilities': {cls: float(p) for cls, p in zip(classes, proba)},
        'pred_idx': pred_idx
    }
