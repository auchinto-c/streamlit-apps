import streamlit as sl
import pandas as pd
import base64
import requests
from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt
import json

# Page Layout
sl.set_page_config(layout='wide')

# Main Panel
sl.title('Crypto 100 - Exploratory Data Analysis')

expanded_bar = sl.expander('About')
expanded_bar.write('Visualizing the % Change for 100 Crypto-currencies over an interval')

col1 = sl.sidebar
col2, col3 = sl.columns((2,1))

# Side Panel
col1.title('User Input Settings')

currency_price_unit = col1.selectbox('Select currency for price', ('USD', 'BTC', 'ETH'))

select_interval = col1.selectbox('Select Interval', ('1h', '24h', '7d'))

interval_map = {
    '1h': 'percent_change_1h',
    '24h': 'percent_change_24h',
    '7d': 'percent_change_7d'
}

# Data
@sl.cache
def getCrypto100():
    url = 'https://coinmarketcap.com'
    data = requests.get(url)
    soup = bs(data.text, 'html.parser')
    data = soup.find('script', id='__NEXT_DATA__', type='application/json')

    coin_data = json.loads(data.contents[0])
    coin_data = json.loads(coin_data['props']['initialState'])
    listings = coin_data['cryptocurrency']['listingLatest']['data']
    
    keys = listings[0]['keysArr']

    rows = []
    for i in listings[1:]:
      rows.append([
        i[keys.index('slug')], 
        i[keys.index('symbol')], 
        i[keys.index(f'quote.{currency_price_unit}.price')], 
        i[keys.index(f'quote.{currency_price_unit}.percentChange1h')],
        i[keys.index(f'quote.{currency_price_unit}.percentChange24h')],
        i[keys.index(f'quote.{currency_price_unit}.percentChange7d')],
        i[keys.index(f'quote.{currency_price_unit}.marketCap')],
        i[keys.index(f'quote.{currency_price_unit}.volume24h')]])

    raw = pd.DataFrame(data=rows, columns=['coin_name', 'coin_symbol', 'market_cap', 'percent_change_1h', 'percent_change_24h', 'percent_change_7d', 'price', 'volume_24h'])
    return raw

crypto100 = getCrypto100()

col2.header('Complete Dataset')
col2.dataframe(crypto100)

def download_csv(df):
    csv = df.to_csv()
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="sp500.csv">Download CSV</a>'
    return href

col2.markdown(download_csv(crypto100), unsafe_allow_html=True)

col2.header(f'Percent Change over {select_interval}')
result = crypto100[['coin_name', interval_map[select_interval]]]
col2.dataframe(result)

# Visualization
result[f'pos_{interval_map[select_interval]}'] = result[interval_map[select_interval]] > 0

result = result.sort_values(interval_map[select_interval])

plt.figure(figsize=(5,25))
plt.subplots_adjust(top = 1, bottom = 0)
result[interval_map[select_interval]].plot(kind='barh', color=result[f'pos_{interval_map[select_interval]}'].map({True: 'g', False: 'r'}))
col3.pyplot(plt)



