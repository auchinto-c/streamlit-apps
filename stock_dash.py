import yfinance as yf
import streamlit as sl
import pandas as pd

sl.write("""
# Stock Dashboard

Showing the **Closing price** and **Volume** for the stock entity : Google
""")

tickerSymbol = 'GOOGL'
tickerData = yf.Ticker(tickerSymbol)
tickerDf = tickerData.history(period='1d', start='2010-5-31', end='2020-5-31')

sl.write("## Closing Price")
sl.line_chart(tickerDf.Close)

sl.write("## Volume")
sl.line_chart(tickerDf.Volume)


