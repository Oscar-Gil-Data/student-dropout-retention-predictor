import streamlit as st

st.set_page_config(
    page_title="Student Dropout & Retention Predictor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Global styles
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'IBM Plex Sans', sans-serif;
    }
    .main-title {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 1.6rem;
        font-weight: 500;
        letter-spacing: -0.02em;
        color: #1a1a2e;
        margin-bottom: 0.2rem;
    }
    .main-subtitle {
        font-size: 0.85rem;
        color: #6b7280;
        font-weight: 300;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: #f8f9fb;
        border-left: 3px solid #e5e7eb;
        padding: 0.9rem 1.1rem;
        border-radius: 4px;
        margin-bottom: 0.6rem;
    }
    .metric-card.dropout  { border-left-color: #378ADD; }
    .metric-card.enrolled { border-left-color: #D85A30; }
    .metric-card.graduate { border-left-color: #639922; }
    .stTabs [data-baseweb="tab"] {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.8rem;
        letter-spacing: 0.05em;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">Student Dropout & Retention Predictor</div>', unsafe_allow_html=True)
st.markdown('<div class="main-subtitle">UCI Dataset &nbsp;·&nbsp; dbt + DuckDB + Python + Streamlit &nbsp;·&nbsp; [oscargildata.com](http://oscargildata.com)</div>', unsafe_allow_html=True)

pg = st.navigation([
    st.Page("pages/01_prediction.py",        title="Prediction",         icon="🎯"),
    st.Page("pages/02_model_performance.py", title="Model Performance",  icon="📊"),
    st.Page("pages/03_eda.py",               title="EDA",                icon="🔍"),
    st.Page("pages/04_about.py",             title="About",              icon="📋"),
])
pg.run()
