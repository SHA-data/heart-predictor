import streamlit as st
import joblib
import numpy as np
from parser import text_extract
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf


model = tf.keras.models.load_model('model.keras')

st.title('Heart Disease Predictor')
st.subheader('Predicts if you could be a heart patient')

metrics_placeholder = st.empty()
prediction_placeholder = st.empty()
visuals_placeholder = st.empty()

age = st.number_input('Enter Age (Years)', max_value = 100)
gender = st.text_input('Gender', help = 'Male or Female?', label_visibility = 'visible')
smoking = st.text_input('Do you Smoke?', help = 'Yes or No?', label_visibility = 'visible')
follow_up = st.number_input("What's your follow_up period for this test? (Tell Days)")

uploaded_file = st.file_uploader('Upload Your Tests Here', type='pdf', key='heart_pdf_uploader')

button = st.button('Submit')

if button is False:
    pass
else:

    if uploaded_file is not None:
        try:
            file_data = text_extract(uploaded_file)
            st.json(file_data)

            if not isinstance(file_data, dict):
                raise ValueError('Parsed PDF data is not a dictionary')

            if any(value is None for value in file_data.values()):
                st.warning('Some PDF fields were not extracted. Check the PDF text format.')

            df = pd.DataFrame([
                {
                    'anaemia': 1 if str(file_data['anaemia']).strip().lower() == 'yes' else 0,
                    'creatinine_phosphokinase': file_data['creatinine_phosphokinase'],
                    'diabetes': 1 if str(file_data['diabetes']).strip().lower() == 'yes' else 0,
                    'ejection_fraction': file_data['ejection_fraction'],
                    'high_blood_pressure': 1 if str(file_data['high_blood_pressure']).strip().lower() == 'yes' else 0,
                    'platelets': file_data['platelets'],
                    'serum_creatinine': file_data['serum_creatinine'],
                    'serum_sodium': file_data['serum_sodium'],
                    'age': age,
                    'gender': 1 if str(gender).strip().lower() == 'woman' else 0,
                    'smoking': 1 if str(smoking).strip().lower() == 'yes' else 0,
                    'time': follow_up
                }
            ])
            
            prediction = model.predict(df)
            with prediction_placeholder.container():
                st.markdown('---')
                st.subheader("Model's prediction")
                st.success('Yes, you better get checked up!' if int(prediction.flatten()[0]) == 1 else "No, there's little worry but a checkup never hurts!")
        except Exception as e:
            st.error(f'Error while parsing or predicting: {e}')
    else:
        st.info('Upload a PDF to get prediction')