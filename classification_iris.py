import streamlit as sl
import pandas as pd
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier

# Sidebar
sl.sidebar.title('Feature Inputs')

def user_input_params():
    select_sl = sl.sidebar.slider('Sepal Length', 4.3, 7.9, 5.4)
    select_sw = sl.sidebar.slider('Sepal Width', 2.0, 4.4, 3.4)
    select_pl = sl.sidebar.slider('Petal Length', 1.0, 6.9, 1.3)
    select_pw = sl.sidebar.slider('Petal Width', 0.1, 2.5, 0.2)

    features = {
        'sepal_length': select_sl,
        'sepal_width': select_sw,
        'petal_length': select_pl,
        'petal_width': select_pw
        }
    
    return pd.DataFrame(features, index=[0])

select_features = user_input_params()

# Data
iris = datasets.load_iris()
X = iris.data
Y = iris.target

# Body
sl.title('Iris Flower Classification')
sl.write(' We predict the Type of flower using 4 features sepal_length, sepal_width, petal_length, petal_width through Random Forest Classifier.')

sl.header('User Input Features')
sl.write(select_features)

sl.header('Classes of Flowers')
sl.table(iris.target_names)

## Model
clf = RandomForestClassifier()
clf.fit(X, Y)

## Predictions
pred_class = clf.predict(select_features)
pred_prob = clf.predict_proba(select_features)

sl.header('Predicted Class')
sl.write(iris.target_names[pred_class])

sl.header('Predicted Probabilities')
sl.table(pred_prob)