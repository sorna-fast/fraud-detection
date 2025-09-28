import streamlit as st
import pandas as pd
import pickle
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_curve,
    auc
)


# Page settings
st.set_page_config(
    page_title="Advanced Fraud Detection System",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load resources
def load_model(filename):
    """Load model from pickle file"""
    with open(filename, 'rb') as f:
        return pickle.load(f)
    
@st.cache_resource
def load_resources():
    try:
        return {
            'model': load_model('./model/gb_classifier.pkl'),
            'X_train': pd.read_csv('./data/split_data/X_train.csv'),
            'y_train': pd.read_csv('./data/split_data/y_train.csv'),
            'X_test': pd.read_csv('./data/split_data/X_test.csv'),
            'y_test': pd.read_csv('./data/split_data/y_test.csv')
        }
    except Exception as e:
        st.error(f"Error loading resources: {str(e)}")
        st.stop()

# Calculate evaluation metrics
def evaluate_model(model, X, y):
    y_pred = model.predict(X)
    y_proba = model.predict_proba(X)[:, 1]
    
    # Classification report
    report = classification_report(y, y_pred, output_dict=True)
    report_df = pd.DataFrame(report).transpose()
    
    # Confusion matrix
    cm = confusion_matrix(y, y_pred)
    
    # ROC curve
    fpr, tpr, thresholds = roc_curve(y, y_proba)
    roc_auc = auc(fpr, tpr)
    
    return {
        'classification_report': report_df,
        'confusion_matrix': cm,
        'roc_curve': (fpr, tpr, roc_auc)
    }

def results_manager():
    resources = load_resources()
    
    st.title("Comprehensive Fraud Detection Model Evaluation")
    
    # Evaluation section
    st.header("Comprehensive Evaluation Results")
    
    # Calculate metrics
    eval_results = evaluate_model(resources['model'], resources['X_test'], resources['y_test'].values.ravel())
    
    # Display ROC curve
    st.subheader("ROC Curve")
    fig_roc = go.Figure()
    fig_roc.add_trace(go.Scatter(
        x=eval_results['roc_curve'][0],
        y=eval_results['roc_curve'][1],
        name=f"ROC Curve (AUC = {eval_results['roc_curve'][2]:.2f})",
        line=dict(color='darkorange', width=2)
    ))
    fig_roc.add_trace(go.Scatter(
        x=[0, 1], y=[0, 1],
        line=dict(color='navy', width=2, dash='dash'),
        name='Random'
    ))
    fig_roc.update_layout(
        xaxis_title='False Positive Rate',
        yaxis_title='True Positive Rate',
        title='Receiver Operating Characteristic (ROC) Curve'
    )
    st.plotly_chart(fig_roc, use_container_width=True)
    
    # Display confusion matrix
    st.subheader("Confusion Matrix")
    cm = eval_results['confusion_matrix']
    fig_cm = px.imshow(
        cm,
        labels=dict(x="Predicted", y="Actual"),
        x=['Legitimate', 'Fraud'],
        y=['Legitimate', 'Fraud'],
        text_auto=True,
        color_continuous_scale='Blues'
    )
    st.plotly_chart(fig_cm, use_container_width=True)
    
    # Display classification report
    st.subheader("Classification Report")
    st.dataframe(
        eval_results['classification_report'].style.format("{:.2f}"),
        use_container_width=True
    )
