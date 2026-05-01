import pandas as pd
import joblib
import os

MODEL_DIR = os.path.join(os.path.dirname(__file__), "../../models/artifacts")

FEATURE_COLUMNS = [
    "sem1_units_approved",
    "sem1_grade",
    "sem2_units_approved",
    "sem2_grade",
    "previous_qualification_grade",
    "admission_grade",
    "age_at_enrollment",
    "tuition_fees_up_to_date",
    "is_scholarship_holder",
    "is_debtor",
]

def build_input_df(**kwargs) -> pd.DataFrame:
    """Build a single-row DataFrame from sidebar inputs in the expected feature order."""
    return pd.DataFrame([{col: kwargs[col] for col in FEATURE_COLUMNS}])


def load_model(model_name: str):
    """Load a serialized model artifact by display name."""
    name_map = {
        "Random Forest": "random_forest.pkl",
        "Logistic Regression": "logistic_regression.pkl",
    }
    path = os.path.join(MODEL_DIR, name_map[model_name])
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Model artifact not found at {path}. "
            "Run notebooks/03_modeling.ipynb to train and save models."
        )
    return joblib.load(path)
