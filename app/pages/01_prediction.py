import streamlit as st
import pandas as pd
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.predict import load_meta, load_model, build_input_df, predict
from utils.shap_utils import get_shap_values, plot_waterfall

CLASS_COLORS = {
    'Dropout':  '#378ADD',
    'Enrolled': '#D85A30',
    'Graduate': '#639922'
}
CLASS_ORDER = ['Dropout', 'Enrolled', 'Graduate']

# ── Load meta and model ──────────────────────────────────────────────
meta   = load_meta()
classes = meta['classes']

st.sidebar.header("Model")
model_name = st.sidebar.selectbox(
    "Classifier",
    ['Random Forest', 'Logistic Regression'],
    index=0,
    help="Random Forest is statistically superior overall. Logistic Regression performs better on the Enrolled class."
)
model = load_model(model_name)

# ── Sidebar: key features ────────────────────────────────────────────
st.sidebar.divider()
st.sidebar.header("Student profile")
st.sidebar.caption("Key features")

sem1_units_approved = st.sidebar.slider("Sem 1 units approved",    0, 26,  5)
sem1_grade          = st.sidebar.slider("Sem 1 grade avg (0-20)",  0, 20, 11)
sem2_units_approved = st.sidebar.slider("Sem 2 units approved",    0, 26,  5)
sem2_grade          = st.sidebar.slider("Sem 2 grade avg (0-20)",  0, 20, 11)
tuition_up_to_date  = st.sidebar.toggle("Tuition fees up to date", value=True)
is_scholarship      = st.sidebar.toggle("Scholarship holder",      value=False)
is_debtor           = st.sidebar.toggle("Debtor",                  value=False)
age_at_enrollment   = st.sidebar.slider("Age at enrollment",      17, 60, 20)

# ── Sidebar: expanded features ───────────────────────────────────────
with st.sidebar.expander("More features"):
    sem1_units_enrolled  = st.slider("Sem 1 units enrolled",   0, 26, 6)
    sem2_units_enrolled  = st.slider("Sem 2 units enrolled",   0, 26, 6)
    sem1_evaluations     = st.slider("Sem 1 evaluations",      0, 45, 6)
    sem2_evaluations     = st.slider("Sem 2 evaluations",      0, 45, 6)
    sem1_units_no_eval   = st.slider("Sem 1 units no eval",    0, 12, 0)
    sem2_units_no_eval   = st.slider("Sem 2 units no eval",    0, 12, 0)
    prev_qual_grade      = st.slider("Prior qual. grade (0-200)", 0, 200, 130)
    application_order    = st.slider("Application order",      1, 9,   1)
    application_mode     = st.number_input("Application mode code", value=1)
    previous_qualification = st.number_input("Previous qualification code", value=1)
    course_id            = st.number_input("Course ID", value=9500)
    attendance_type      = st.selectbox("Attendance", [1, 0], format_func=lambda x: "Daytime" if x == 1 else "Evening")
    nationality          = st.number_input("Nationality code", value=1)
    gender               = st.selectbox("Gender", [1, 0], format_func=lambda x: "Male" if x == 1 else "Female")
    is_international     = st.toggle("International student", value=False)
    is_displaced         = st.toggle("Displaced", value=False)
    has_special_needs    = st.toggle("Special educational needs", value=False)
    marital_status       = st.number_input("Marital status code", value=1)
    mothers_qualification = st.number_input("Mother's qualification code", value=1)
    fathers_qualification = st.number_input("Father's qualification code", value=1)
    mothers_occupation   = st.number_input("Mother's occupation code", value=1)
    fathers_occupation   = st.number_input("Father's occupation code", value=1)
    unemployment_rate    = st.number_input("Unemployment rate", value=10.8)
    inflation_rate       = st.number_input("Inflation rate", value=1.4)
    gdp                  = st.number_input("GDP", value=1.74)

# ── Build feature dict ───────────────────────────────────────────────
sem1_approval_rate = sem1_units_approved / sem1_units_enrolled if sem1_units_enrolled > 0 else 0.0
sem2_approval_rate = sem2_units_approved / sem2_units_enrolled if sem2_units_enrolled > 0 else 0.0

feature_values = {
    'marital_status':              marital_status,
    'application_mode':            application_mode,
    'application_order':           application_order,
    'course_id':                   course_id,
    'attendance_type':             attendance_type,
    'previous_qualification':      previous_qualification,
    'previous_qualification_grade': prev_qual_grade,
    'nationality':                 nationality,
    'gender':                      gender,
    'age_at_enrollment':           age_at_enrollment,
    'is_international':            int(is_international),
    'is_displaced':                int(is_displaced),
    'mothers_qualification':       mothers_qualification,
    'fathers_qualification':       fathers_qualification,
    'mothers_occupation':          mothers_occupation,
    'fathers_occupation':          fathers_occupation,
    'is_scholarship_holder':       int(is_scholarship),
    'tuition_fees_up_to_date':     int(tuition_up_to_date),
    'is_debtor':                   int(is_debtor),
    'has_special_needs':           int(has_special_needs),
    'sem1_units_enrolled':         sem1_units_enrolled,
    'sem1_evaluations':            sem1_evaluations,
    'sem1_units_approved':         sem1_units_approved,
    'sem1_grade':                  sem1_grade,
    'sem1_units_no_eval':          sem1_units_no_eval,
    'sem2_units_enrolled':         sem2_units_enrolled,
    'sem2_evaluations':            sem2_evaluations,
    'sem2_units_approved':         sem2_units_approved,
    'sem2_grade':                  sem2_grade,
    'sem2_units_no_eval':          sem2_units_no_eval,
    'unemployment_rate':           unemployment_rate,
    'inflation_rate':              inflation_rate,
    'gdp':                         gdp,
    'sem1_approval_rate':          sem1_approval_rate,
    'sem2_approval_rate':          sem2_approval_rate,
    'units_approved_delta':        sem2_units_approved - sem1_units_approved,
    'grade_delta':                 sem2_grade - sem1_grade,
    'combined_approval_rate':      (sem1_approval_rate + sem2_approval_rate) / 2,
    'financial_stress':            int(is_debtor and not tuition_up_to_date),
}

input_df = build_input_df(feature_values, meta)
result   = predict(model, input_df, classes)
pred     = result['prediction']
proba    = result['probabilities']
pred_idx = result['pred_idx']

# ── Main content ─────────────────────────────────────────────────────
color = CLASS_COLORS[pred]
st.markdown(
    f"<h2 style='color:{color}; font-family:IBM Plex Mono,monospace; margin-bottom:0.2rem;'>"
    f"Predicted outcome: {pred}</h2>",
    unsafe_allow_html=True
)
st.caption(f"Model: {model_name}")
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Class probabilities")
    for cls in CLASS_ORDER:
        p = proba[cls]
        bar_color = CLASS_COLORS[cls]
        st.markdown(
            f"<div style='margin-bottom:10px;'>"
            f"<div style='display:flex;justify-content:space-between;margin-bottom:3px;'>"
            f"<span style='font-size:0.85rem;font-weight:500;color:#374151;'>{cls}</span>"
            f"<span style='font-size:0.85rem;font-weight:600;color:{bar_color};'>{p:.1%}</span>"
            f"</div>"
            f"<div style='background:#f3f4f6;border-radius:3px;height:10px;'>"
            f"<div style='background:{bar_color};width:{p*100:.1f}%;height:100%;border-radius:3px;'></div>"
            f"</div></div>",
            unsafe_allow_html=True
        )

with col2:
    st.markdown("#### SHAP feature impact")
    st.caption(f"Explaining the **{pred}** prediction")
    try:
        shap_values = get_shap_values(model, model_name, input_df)
        plot_waterfall(shap_values, pred_idx, pred)
    except Exception as e:
        st.info(f"SHAP explanation unavailable: {e}")

st.divider()
st.markdown("#### Interpretation")

interp_map = {
    'Dropout': (
        "This student profile shows elevated dropout risk. "
        "The features with the longest red bars above are the strongest contributors. "
        "Tuition status and first semester performance are typically the dominant signals. "
        "Early outreach and financial support intervention are recommended."
    ),
    'Enrolled': (
        "This student is predicted to remain enrolled but not yet graduate. "
        "This is the most uncertain outcome -- the model has lower confidence here "
        "than for Dropout or Graduate predictions. Monitor academic trajectory closely."
    ),
    'Graduate': (
        "This student profile is consistent with successful graduation. "
        "Strong semester performance and financial stability are the primary drivers. "
        "Continue current support structures."
    )
}
st.markdown(interp_map[pred])
