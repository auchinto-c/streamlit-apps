import streamlit as sl
import pandas as pd
import base64
import yfinance as yf

# Data
@sl.cache
def getSP500():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html = pd.read_html(url, header=0)
    raw = html[0]
    df = raw.drop(columns=['SEC filings'])
    return df

sp500 = getSP500()

sectors = sorted(sp500['GICS Sector'].unique())

# Side Panel

sl.sidebar.title('User Input Settings')

select_sector = sl.sidebar.multiselect('GICS Sectors', sectors, sectors)

select_num_comp = sl.sidebar.select_slider('# Companies', list(range(1, 6)), 1)

# Main Panel

sl.title('S&P 500 - Exploratory Data Analysis')
sl.write('Visualizing the Closing Price for S&P 500 Companies by GICS Sector')

sl.write('Select the sectors to group by and fetch the first N companies to create the plots')

select_data = sp500[(sp500['GICS Sector'].isin(select_sector))]
grp_data = select_data.groupby('GICS Sector')
data = grp_data.first()
sl.write(f'Data Dimension: {data.shape[0]} rows {data.shape[1]} cols')
sl.dataframe(data)

def download_csv(df):
    csv = df.to_csv()
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="sp500.csv">Download CSV</a>'
    return href

sl.markdown(download_csv(sp500), unsafe_allow_html=True)

# Visualization
sector = sl.selectbox('Select GICS Sector', sectors)

if sl.button('Plot Company Closing values'):
    tickerSymbols = grp_data.get_group(sector)['Symbol'][:select_num_comp]

    for tickerSymbol in tickerSymbols:
        tickerData = yf.Ticker(tickerSymbol)
        tickerDf = tickerData.history(period='1d', start='2010-5-31', end='2020-5-31')

        close_val = tickerDf['Close']

        sl.write(f'## {tickerSymbol}')
        sl.line_chart(close_val)
