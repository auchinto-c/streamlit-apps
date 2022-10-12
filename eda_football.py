import streamlit as sl
import pandas as pd
import numpy as np
import base64
import seaborn as sns
import matplotlib.pyplot as plt

# Sidebar - Year

sl.sidebar.title('User Input Settings')

selected_year = sl.sidebar.selectbox('Year', list(reversed(range(1970, 2022))))

# Scraping Data
@sl.cache
def getProFootballRushingStats(year):
    url = f'https://www.pro-football-reference.com/years/{year}/rushing.htm'
    html = pd.read_html(url, header=1)
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index)
    raw.Pos = raw.Pos.fillna('N/A').apply(lambda x: x.upper())
    raw = raw.fillna(0)
    stats = raw.drop(['Rk'], axis=1)
    return stats

stats = getProFootballRushingStats(selected_year)

teams = sorted(stats.Tm.unique())
positions = sorted(stats.Pos.unique())

# Sidebar - Teams
selected_teams = sl.sidebar.multiselect('Teams', teams, teams)

# Sidebar - Positions
selected_pos = sl.sidebar.multiselect('Positions', positions, positions)

# Body
sl.title('Pro Football Rushing Stats')

sl.write('This app displays the pro-football rushing player stats')

sl.header('Dataframe')

select_stats = stats[(stats.Tm.isin(selected_teams)) & (stats.Pos.isin(selected_pos))]

sl.write(f'Data Dimension {select_stats.shape[0]} rows {select_stats.shape[1]} cols')

sl.dataframe(select_stats)

# Download as CSV

def download_csv(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV</a>'
    return href

sl.markdown(download_csv(select_stats), unsafe_allow_html=True)

# Visualization

if sl.button('Correlation Heatmap'):
    sl.header('Correlation Heatmap')
    select_stats.to_csv('output.csv', index=False)

    df = pd.read_csv('output.csv')

    corr = df.corr()

    f, ax = plt.subplots(figsize=(7,5))
    sns.heatmap(corr)

    sl.pyplot(f)
