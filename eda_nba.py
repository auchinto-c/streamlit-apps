import streamlit as sl
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import base64

# Sidebar - Header
sl.sidebar.title('User Input Settings')

selected_year = sl.sidebar.selectbox('Year', list(reversed(range(1950, 2020))))

# Scraping data
@sl.cache
def captureNBAStats(year):
    url = f"https://www.basketball-reference.com/leagues/NBA_{year}_per_game.html"
    html = pd.read_html(url, header = 0)
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index)
    raw = raw.fillna(0)
    stats = raw.drop(['Rk'], axis=1)
    return stats

stats = captureNBAStats(selected_year)

teams = sorted(stats.Tm.unique())
positions = sorted(stats.Pos.apply(lambda x: x.split('-')[0] if '-' in x else x).unique())

# Sidebar - Body
selected_teams = sl.sidebar.multiselect('Teams', teams, teams)

selected_pos = sl.sidebar.multiselect('Positions', positions, positions)

# Body

sl.title('NBA Player Stats')

sl.write('This app performs simple web scraping of NBA player stats data')

sl.header('Display Player Stats of Selected Team(s)')

stats = stats[(stats.Tm.isin(selected_teams)) & (stats.Pos.isin(selected_pos))]

sl.write(f'Data Dimensions: {stats.shape[0]} rows {stats.shape[1]} columns')
sl.dataframe(stats)

# Download as CSV

def download_csv(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV</a>'
    return href

sl.markdown(download_csv(stats), unsafe_allow_html=True)

# Visualization

if sl.button('Correlation Heatmap'):
    sl.header('Heatmap')
    stats.to_csv('output.csv', index=False)
    df = pd.read_csv('output.csv')

    corr = df.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True

    print(mask)
    f, ax = plt.subplots(figsize=(7, 5))
    with sns.axes_style('white'):
        ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)

    sl.pyplot(f)