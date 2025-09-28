import streamlit as st
import pandas as pd
import pickle

def main_predictor():
    # Application title
    st.title('Predicting fraud in financial transactions')  # 'Financial Transaction Fraud Prediction'
    
    # Cache the model loading to improve performance
    @st.cache_resource
    def load_model():
        """Load the trained model from pickle file"""
        with open('./model/gb_classifier.pkl', 'rb') as f:
            model = pickle.load(f)
        return model

    # Load the model
    model = load_model()
    
    # Extract components from the pipeline
    transformer = model.named_steps['transformer']

    # Get all feature names
    try:
        all_columns = transformer.feature_names_in_
    except AttributeError:
        st.error("Model is outdated and doesn't support feature_names_in_!")
        st.stop()

    # Get transformed columns from each transformer
    numeric_cols = transformer.transformers_[0][2]      # StandardScaler columns
    category_cols = transformer.transformers_[1][2]     # OrdinalEncoder columns
    binary_cols = transformer.transformers_[2][2]       # OneHotEncoder columns

    # Calculate remainder columns
    transformed_cols = set(numeric_cols + category_cols + binary_cols)
    remainder_cols = [col for col in all_columns if col not in transformed_cols]

    # Get encoding information for categorical features
    ordinal_encoder = transformer.named_transformers_['OrdinalEncoder']
    category_options = {
        col: values.tolist() 
        for col, values in zip(category_cols, ordinal_encoder.categories_)
    }

    # Get encoding information for binary feature
    ohe_encoder = transformer.named_transformers_['onehot']
    binary_options = ohe_encoder.categories_[0].tolist()

    # User input section
    st.header('Information input')  # 'Input Data'
    inputs = {}

    # Numerical inputs
    st.subheader('Numerical values')  # 'Numerical Values'
    for col in numeric_cols:
        inputs[col] = st.number_input(col, value=0.0, format="%.2f")

    # Categorical inputs
    st.subheader('Batch values')  # 'Categorical Values'
    for col in category_cols:
        inputs[col] = st.selectbox(col, category_options[col])

    # Binary input
    st.subheader('Weekend status')  # 'Weekend Status'
    inputs[binary_cols[0]] = st.selectbox(binary_cols[0], binary_options)

    # Remainder inputs (temporal features)
    st.subheader('Other time information')  # 'Other Temporal Information'
    for col in remainder_cols:
        if col == "Transaction_Hour":
            inputs[col] = st.slider("Transaction Hour", 0, 23, 12)  # 'Transaction Hour'
        elif col == "Transaction_Month":
            inputs[col] = st.slider("Transaction Month", 1, 12, 6)  # 'Transaction Month'
        elif col == "Transaction_Day":
            inputs[col] = st.slider("Transaction Day", 1, 31, 15)  # 'Transaction Day'
        elif col == "Transaction_DayOfWeek":
            inputs[col] = st.slider("Day of the week (0=Saturday, 6=Friday)", 0, 6, 3)  # 'Day of Week'

    # Prediction button
    if st.button('Predicting fraud'):  # 'Predict Fraud'
        try:
            # Create input DataFrame ensuring correct column order
            input_df = pd.DataFrame([inputs]).reindex(columns=all_columns)
            
            # Make prediction
            prediction = model.predict(input_df)[0]
            proba = model.predict_proba(input_df)[0][1]  # Probability of fraud
            
            # Display results
            st.header('Results')  
            if prediction >= 0.75:
                st.error(f'Result: Fraud')
            else :
                st.success('Healthy transaction')  
                  # 'Result: {result}'
            st.info(f'Probability of fraud: {proba:.2%}')  # 'Fraud Probability: {proba:.2%}'
            
            # Add visual indicators
            if prediction == 1:
                st.warning('Warning: This transaction has been detected as risky!')  # 'Warning: High-risk transaction detected!'
            else:
                st.balloons()
                
        except Exception as e:
            st.error(f'Error processing: {str(e)}')  # 'Processing Error: {str(e)}'

