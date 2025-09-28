import streamlit as st
from apps.src import main_predictor,results_manager

# Initialize session state for page navigation
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

# Custom CSS for responsive styling
st.markdown("""
    <style>
    .main {background-color: #f5f5f5;}
    .stButton>button {
        width: 100%;
        height: 80px;
        border-radius: 10px;
        font-size: 20px !important;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .title {text-align: center; color: #1e3a8a;}
    </style>
""", unsafe_allow_html=True)

def home_page():
    """Main landing page with navigation options"""
    st.markdown("<h1 class='title'>Smart Fraud Detection with Gradient Boosting</h1>", unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Center-aligned navigation buttons
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<h3 style='text-align: center; color: #2d3436;'>Select an option</h3>", unsafe_allow_html=True)
        
        # Split buttons into two columns
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("🎯 Make Prediction", help="Click to make new fraud predictions"):
                st.session_state.current_page = 'prediction'
                st.rerun()
        with btn_col2:
            if st.button("📊 View Results", help="View model evaluation metrics"):
                st.session_state.current_page = 'results'
                st.rerun()

def prediction_page():
    """Prediction interface page"""
    st.markdown("<h1 class='title'>Prediction Dashboard</h1>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("---")
        main_predictor() # Prediction module
        st.markdown("---")
        
        # Centered return button
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            if st.button("🏠 Return Home", type='secondary'):
                st.session_state.current_page = 'home'
                st.rerun()

def results_page():
    """Model performance results page"""
    st.markdown("<h1 class='title'>Model Analytics</h1>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("---")
        results_manager()  # Results module
        st.markdown("---")
        
        # Centered return button
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            if st.button("🏠 Return Home", type='secondary'):
                st.session_state.current_page = 'home'
                st.rerun()

# Page router
if st.session_state.current_page == 'home':
    home_page()
elif st.session_state.current_page == 'prediction':
    prediction_page()
elif st.session_state.current_page == 'results':
    results_page()

# App description section
st.markdown("""
## Application Overview

### Results Dashboard
Displays model performance metrics and evaluation results on test data.

### Prediction Interface
Allows users to input transaction details and receive real-time fraud probability predictions.
""")