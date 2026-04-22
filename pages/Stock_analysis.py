import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import datetime
import ta
from dateutil.utils import today
from pages.utils.plotly_figure import plotly_table
# Agar file ka naam indicators.py hai
from pages.utils.plotly_figure import candlestick, RSI, MACD, close_chart, Moving_average, filter_data,Moving_average_forecast

st.set_page_config(page_title='Stock Analysis',
                   page_icon='page_with_curl',
                   layout='wide')
st.title('Stock Analysis')

col1,col2,col3=st.columns(3)
todays = datetime.date.today()   # 🔥 yaha naam match karo

with col1:
    ticker = st.text_input('Stock Ticker', 'TSLA')

with col2:
    start_date = st.date_input(
        'Choose Start Date',
        datetime.date(todays.year - 1, todays.month, todays.day)
    )

with col3:
    end_date = st.date_input(
        'Choose End Date',
        datetime.date(todays.year, todays.month, todays.day)
    )

st.subheader(ticker)
stock=yf.Ticker(ticker)

st.write(stock.info['longBusinessSummary'])
st.write("**Sector:**",stock.info['sector'])
st.write("**Full Time Employees:**",stock.info['fullTimeEmployees'])
st.write("**Website:**",stock.info['website'])


col1, col2 = st.columns(2)


with col1:

    df = pd.DataFrame(index=['Market Cap', 'Beta', 'EPS', 'PE Ratio'])
    df[''] = [
        stock.info.get("marketCap"),
        stock.info.get("beta"),
        stock.info.get("trailingEps"),
        stock.info.get("trailingPE")
    ]

    fig_df = plotly_table(df)
    st.plotly_chart(fig_df, use_container_width=True)

with col2:
    df = pd.DataFrame(index=[
        'Quick Ratio',
        'Revenue per share',
        'Profit Margins',
        'Debt to Equity',
        'Return on Equity'
    ])
    df[''] = [
        stock.info.get("quickRatio"),
        stock.info.get("revenuePerShare"),
        stock.info.get("profitMargins"),
        stock.info.get("debtToEquity"),
        stock.info.get("returnOnEquity")
    ]


    fig_df = plotly_table(df)
    st.plotly_chart(fig_df, use_container_width=True)

data =yf.download(ticker,start=start_date,end=end_date)

# 1. Flatten the columns to remove the ('Close', 'TSLA') tuple format
data.columns = [col[0] for col in data.columns]

col1, col2, col3 = st.columns(3)

# 2. Calculate daily change (ensure we get a single float value, not a Series)
last_price = float(data['Close'].iloc[-1])
prev_price = float(data['Close'].iloc[-2])
daily_change = last_price - prev_price

# 3. Display the metric without the 'dtype' text
col1.metric("Daily Change", f"{last_price:.2f}", f"{daily_change:.2f}")

# 4. Prepare the table for display
last_10_df = data.tail(10).sort_index(ascending=False).round(3)

# If your plotly_table function handles the dataframe, call it here
fig_df = plotly_table(last_10_df)

st.write('##### Historical Data (Last 10 days)')
st.plotly_chart(fig_df, use_container_width=True)

col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12 = st.columns([1,1,1,1,1,1,1,1,1,1,1,1])

num_period = ''

with col1:
    if st.button('5D'):
        num_period = '5d'
with col2:
    if st.button('1M'):
        num_period = '1mo'
with col3:
    if st.button('6M'):
        num_period = '6mo'
with col4:
    if st.button('YTD'):
        num_period = 'ytd'
with col5:
    if st.button('1Y'):
        num_period = '1y'
with col6:
    if st.button('5Y'):
        num_period = '5y'
with col7:
    if st.button('MAX'):
        num_period = 'max'

coll, col2, col3 = st.columns([1, 1, 4])
with coll:
    chart_type = st.selectbox('', ('Candle', 'Line'))
with col2:
    if chart_type == 'Candle':

        indicators = st.selectbox('', ('RSI', 'MACD'))
    else:
        indicators = st.selectbox('', ('RSI', 'Moving Average', 'MACD'))

ticker_ = yf.Ticker(ticker)
new_df1 = ticker_.history(period='max')
data1 = ticker_.history(period='max')

if num_period == '':

    if chart_type == 'Candle' and indicators == 'RSI':
        st.plotly_chart(candlestick(data1, '1y'), use_container_width=True)
        st.plotly_chart(RSI(data1, '1y'), use_container_width=True)

    if chart_type == 'Candle' and indicators == 'MACD':
        st.plotly_chart(candlestick(data1, '1y'), use_container_width=True)
        st.plotly_chart(MACD(data1, '1y'), use_container_width=True)

    if chart_type == 'Line' and indicators == 'RSI':
        st.plotly_chart(close_chart(data1, '1y'), use_container_width=True)
        st.plotly_chart(RSI(data1, '1y'), use_container_width=True)

    if chart_type == 'Line' and indicators == 'Moving Average':
        st.plotly_chart(Moving_average(data1, '1y'), use_container_width=True)

    if chart_type == 'Line' and indicators == 'MACD':
        st.plotly_chart(close_chart(data1, '1y'), use_container_width=True)
        st.plotly_chart(MACD(data1, '1y'), use_container_width=True)

else:

    if chart_type == 'Candle' and indicators == 'RSI':
        st.plotly_chart(candlestick(new_df1, num_period), use_container_width=True)
        st.plotly_chart(RSI(new_df1, num_period), use_container_width=True)

    if chart_type == 'Candle' and indicators == 'MACD':
        st.plotly_chart(candlestick(new_df1, num_period), use_container_width=True)
        st.plotly_chart(MACD(new_df1, num_period), use_container_width=True)

    if chart_type == 'Line' and indicators == 'RSI':
        st.plotly_chart(close_chart(new_df1, num_period), use_container_width=True)
        st.plotly_chart(RSI(new_df1, num_period), use_container_width=True)

    if chart_type == 'Line' and indicators == 'Moving Average':
        st.plotly_chart(Moving_average(new_df1, num_period), use_container_width=True)

    if chart_type == 'Line' and indicators == 'MACD':
        st.plotly_chart(close_chart(new_df1, num_period), use_container_width=True)
        st.plotly_chart(MACD(new_df1, num_period), use_container_width=True)

