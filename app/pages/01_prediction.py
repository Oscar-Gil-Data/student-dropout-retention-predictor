import streamlit as st
import pandas as pd
import shap
import joblib
import matplotlib.pyplot as plt

from utils.predict import build_input_df, load_model
from utils.shap_utils import get_shap_values, plot_waterfall

st.set_page_config(page_title="Prediction", layout="wide")
st.title("Live Prediction")
st.markdown("Adjust the student profile in the sidebar and see the model's prediction update in real time.")

# --- Sidebar inputs ---
st.sidebar.header("Student profile")

sem1_units_approved = st.sidebar.slider("1st sem. units approved", 0, 26, 5)
sem1_grade = st.sidebar.slider("1st sem. grade avg (0–200)", 0, 200, 110)
sem2_units_approved = st.sidebar.slider("2nd sem. units approved", 0, 26, 5)
sem2_grade = st.sidebar.slider("2nd sem. grade avg (0–200)", 0, 200, 110)
previous_qualification_grade = st.sidebar.slider("Previous qualification grade (0–200)", 0, 200, 122)
admission_grade = st.sidebar.slider("Admission grade (0–200)", 0, 200, 130)
age_at_enrollment = st.sidebar.slider("Age at enrollment", 17, 60, 22)
tuition_fees_up_to_date = st.sidebar.toggle("Tuition fees up to date", value=True)
is_scholarship_holder = st.sidebar.toggle("Scholarship holder", value=False)
is_debtor = st.sidebar.toggle("Debtor", value=False)

st.sidebar.divider()
model_choice = st.sidebar.selectbox("Model", ["Random Forest", "Logistic Regression"])

# --- Build input and predict ---
input_df = build_input_df(
    sem1_units_approved=sem1_units_approved,
    sem1_grade=sem1_grade,
    sem2_units_approved=sem2_units_approved,
    sem2_grade=sem2_grade,
    previous_qualification_grade=previous_qualification_grade,
    admission_grade=admission_grade,
    age_at_enrollment=age_at_enrollment,
    tuition_fees_up_to_date=int(tuition_fees_up_to_date),
    is_scholarship_holder=int(is_scholarship_holder),
    is_debtor=int(is_debtor),
)

model = load_model(model_choice)
proba = model.predict_proba(input_df)[0]
classes = model.classes_
prediction = classes[proba.argmax()]

# --- Prediction header ---
color_map = {"Dropout": "🔴", "Enrolled": "🔵", "Graduate": "🟢"}
st.subheader(f"Predicted outcome: {color_map.get(prediction, '')} **{prediction}**")

# --- Probability bars ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Class probabilities")
    for cls, prob in zip(classes, proba):
        st.metric(label=cls, value=f"{prob:.1%}")

with col2:
    st.markdown("#### SHAP feature impact")
    # Placeholder — replace with shap waterfall once model artifacts exist
    st.info("SHAP chart renders here after model artifacts are trained and saved.")

# --- Interpretation ---
st.divider()
st.markdown("#### What's driving this prediction?")
st.markdown(
    """
    Red SHAP values push the prediction toward **Dropout**.
    Green values push toward **Graduate** or **Enrolled**.
    The features with the longest bars have the most influence on this specific student's prediction.
    """
)
