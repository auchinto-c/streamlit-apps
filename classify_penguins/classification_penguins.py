import streamlit as sl
import pickle as pkl
import pandas as pd
import base64
from sklearn.ensemble import RandomForestClassifier
import os

# -------------------------- #
# Sidebar
# -------------------------- #
sl.sidebar.title('User Input Features')
## File Upload
sl.sidebar.header('Input using file')

def download_example(df, train=False):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()

    title = 'example_input' if not train else 'example_dataset'
    label = 'Example Input Feature CSV Download' if not train else 'Example Dataset CSV Download'

    href = f'<a href="data:file/csv;base64,{b64}" download="{title}.csv">{label}</a>'
    return href

example_input = pd.DataFrame([('Biscoe', 'male', 45.0, 15.0, 200, 4500)], columns=['island', 'sex', 'bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g'])
sl.sidebar.markdown(download_example(example_input), unsafe_allow_html=True)

input_csv = sl.sidebar.file_uploader('Input Features (.csv)', 'csv')

## Custom Inputs
sl.sidebar.header('Custom Input')

island = sl.sidebar.selectbox('Island', ['Biscoe', 'Dream', 'Torgersen'])
sex = sl.sidebar.selectbox('Sex', ['male', 'female'])
bill_length = sl.sidebar.slider('Bill Length (mm)', 30.0, 60.0, 40.0)
bill_depth = sl.sidebar.slider('Bill Depth (mm)', 10.0, 25.0, 15.0)
flipper_length = sl.sidebar.slider('Flipper Length (mm)', 150, 250, 200)
body_mass = sl.sidebar.slider('Body Mass (g)', 2500, 7000, 4500)

# -------------------------- #
# Body
# -------------------------- #
sl.title('Classification of Penguins')
sl.write('This app trains the classifier and saves it to be reused.')

## Data
raw_data = pd.read_csv('penguins_cleaned.csv')

sl.markdown(download_example(raw_data, True), unsafe_allow_html=True)

input_dataset = sl.file_uploader('Input Dataset (.csv)', 'csv')

if input_dataset is not None:
    raw_data = pd.read_csv(input_dataset)

target = 'species'
encode = ['sex', 'island']

data = raw_data.drop(columns=[target])

def encodeCols(df, encode):
    for col in encode:
        dummy = pd.get_dummies(df[col], prefix=col)
        df = pd.concat([df, dummy], axis=1)
        del df[col]
    return df

## Training
if sl.button('Train the model'):
    X = encodeCols(data, encode)
    Y = raw_data[target]

    clf = RandomForestClassifier()
    clf.fit(X, Y)

    pkl.dump(clf, open('penguin_clf.pkl', 'wb'))
    sl.write('Training Completed')


## User Input Features
sl.header('User Input Features')

if input_csv is not None:
    input_df = pd.read_csv(input_csv)
else:
    features = {
        'island': island,
        'sex': sex,
        'bill_length_mm': bill_length,
        'bill_depth_mm': bill_depth,
        'flipper_length_mm': flipper_length,
        'body_mass_g': body_mass
    }
    input_df = pd.DataFrame(features, index=[0])

sl.write(input_df)

sl.header('Model Input Features')

df = pd.concat([input_df, data], axis=0)
df = encodeCols(df, encode)
df = df[:1]

sl.write(df)

## Labels
sl.header('Labels')
labels = sorted(raw_data[target].unique())
sl.write(labels)

## Predictions
if os.path.exists('penguin_clf.pkl'):
    clf = pkl.load(open('penguin_clf.pkl', 'rb'))

    pred_class = clf.predict(df)
    pred_prob = clf.predict_proba(df)

    sl.header('Prediction Class')
    sl.write(pred_class)

    sl.header('Prediction Probabilities')
    sl.write(pred_prob)