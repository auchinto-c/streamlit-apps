import streamlit as sl
import pandas as pd
import shap
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.ensemble import RandomForestRegressor

sl.title('Boston House Price Predictor')

# Data
boston = datasets.load_boston()
X = pd.DataFrame(boston.data, columns=boston.feature_names)
Y = pd.DataFrame(boston.target, columns=['MEDV'])

# Sidebar
sl.sidebar.header('Specify Input Parameters')

def user_input_features():
    CRIM = sl.sidebar.slider('CRIM', X.CRIM.min(), X.CRIM.max(), float(X.CRIM.mean()))
    ZN = sl.sidebar.slider('ZN', X.ZN.min(), X.ZN.max(), float(X.ZN.mean()))
    INDUS = sl.sidebar.slider('INDUS', X.INDUS.min(), X.INDUS.max(), float(X.INDUS.mean()))
    CHAS = sl.sidebar.slider('CHAS', X.CHAS.min(), X.CHAS.max(), float(X.CHAS.mean()))
    NOX = sl.sidebar.slider('NOX', X.NOX.min(), X.NOX.max(), float(X.NOX.mean()))
    RM = sl.sidebar.slider('RM', X.RM.min(), X.RM.max(), float(X.RM.mean()))
    AGE = sl.sidebar.slider('AGE', X.AGE.min(), X.AGE.max(), float(X.AGE.mean()))
    DIS = sl.sidebar.slider('DIS', X.DIS.min(), X.DIS.max(), float(X.DIS.mean()))
    RAD = sl.sidebar.slider('RAD', X.RAD.min(), X.RAD.max(), float(X.RAD.mean()))
    TAX = sl.sidebar.slider('TAX', X.TAX.min(), X.TAX.max(), float(X.TAX.mean()))
    PTRATIO = sl.sidebar.slider('PTRATIO', X.PTRATIO.min(), X.PTRATIO.max(), float(X.PTRATIO.mean()))
    B = sl.sidebar.slider('B', X.B.min(), X.B.max(), float(X.B.mean()))
    LSTAT = sl.sidebar.slider('LSTAT', X.LSTAT.min(), X.LSTAT.max(), float(X.LSTAT.mean()))

    data = {'CRIM': CRIM, 'ZN': ZN, 'INDUS': INDUS, 'CHAS':CHAS, 'NOX':NOX, 'RM':RM,
     'AGE':AGE, 'DIS':DIS, 'RAD':RAD, 'TAX':TAX, 'PTRATIO':PTRATIO, 'B':B, 'LSTAT':LSTAT}

    features = pd.DataFrame(data, index=[0])

    return features

df = user_input_features()

# Body

sl.header('Specified Input Parameters')
sl.write(df)
sl.write('***')

# Model
model = RandomForestRegressor()
model.fit(X, Y)

# Prediction
prediction = model.predict(df)

sl.header('Prediction of MEDV')
sl.write(prediction)
sl.write('---')

# Explanation
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X)

sl.header('Feature Importance')

f, ax = plt.subplots()

plt.title('Feature Importance based on SHAP values')
shap.summary_plot(shap_values, X)
sl.pyplot(f, bbox_inches='tight')
sl.write('---')

f1, ax1 = plt.subplots()
plt.title('Feature importance based on SHAP values (Bar)')
shap.summary_plot(shap_values, X, plot_type='bar')
sl.pyplot(f1, bbox_inches='tight')