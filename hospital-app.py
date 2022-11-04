import pandas as pd
import streamlit as st
import datetime as dt
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import Lasso
import pickle
import warnings
warnings.filterwarnings('ignore')

encode = {
    'smoker':{'Yes':1, 'No':0}, 'sex':{'Male':1, 'Female':0}
}

#df_orig = pd.read_csv("./apollo_data.csv")
#print(df_orig)
#st.dataframe(df_orig)
def model_pred(age:int=25, viral_load:float=1, severity_level:int=1, smoker=0, sex_male=0, region_northwest=0, region_southeast=0, region_southwest=0):

    #with open(r'C:\Users\Nischay\polyreg', 'rb') as file:
    poly_model = pickle.load(open(r'C:\Users\Nischay\polyreg', 'rb'))
    
    #with open(r'C:\Users\Nischay\hospital_LR_L1_model', 'rb') as file:
    reg_model = pickle.load(open(r'C:\Users\Nischay\hospital_LR_L1_model', 'rb'))

    raw_input = np.array([[age, viral_load, severity_level, smoker, sex_male, region_northwest, region_southeast, region_southwest, 1]])
    transformed_input = poly_model.transform(raw_input)

    pred = reg_model.predict(transformed_input)

    return int(pred)

#print(model_pred(40, 5.42, 2, 0,1,0,0,1))

### Page setting ###

if "horizontal" not in st.session_state:
    st.session_state.horizontal = True

st.set_page_config(layout='wide')

st.title('Hospitalization Charge Estimation Portal')

col1, col2 = st.columns(2)

age = col1.slider("Set the age below", 1,110,1)

viral_load = col2.slider("Set the viral load below", 3.0,25.0,0.1)

severity_level = col2.radio('Select severity level', [0,1,2,3,4,5], key="horizontal", horizontal = st.session_state.horizontal)

smoke = col2.radio('Do you smoke?', ['Yes', 'No'])

gender = col1.radio('Select your gender', ['Male', 'Female'])

region = col1.selectbox('Please select your region', ['Northeast','Northwest', 'Southeast', 'Southwest'])

sex_male = encode['sex'][gender]
smoker = encode['smoker'][smoke]

if(st.button("Get Estimated Hospitalization Charge")):

    region_northwest, region_southeast, region_southwest = 0,0,0

    if region=='Northwest': 
        region_northwest=1
    elif region == 'Southeast': 
        region_southeast=1
    elif region == 'Southwest': 
        region_southwest=1

    charge = model_pred(age, viral_load, severity_level, smoker, sex_male, region_northwest, region_southeast, region_southwest)
    #print(charge)
    st.text("Estimated Charge for the patient is: Rs "+str(charge))




