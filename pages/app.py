import streamlit as st
import pandas as pd
import yfinance as yf
# app.py ke top par ye likhein
import pages.Capm_function as Capm_function
from pages.Capm_function import normalize

st.set_page_config(page_title='CAPM',
                   page_icon='chart_with_upwards_trends',
                   layout='wide')
st.title('Capital Asset Pricing Model')
col1,col2=st.columns([1,1])
with col1:
    stock_list = st.multiselect('Choose 4 Stocks', ('AMZN', 'NFLX', 'TSLA', 'AAPL', 'MSFT', 'NVDA', 'MGM', 'GOOGL'),
                                ['TSLA', 'AAPL', 'AMZN', 'GOOGL'])
with col2:
    years = st.number_input('Number of years', 1, 10)


import datetime
end=datetime.date.today()
start=datetime.date(datetime.date.today().year-years,datetime.date.today().month,datetime.date.today().day)

# 'sp500' FRED ka ticker hai, yfinance mein iska ticker '^GSPC' hota hai
SP500 = yf.download('^GSPC', start=start, end=end)
SP500.columns = SP500.columns.get_level_values(0)
# print(SP500.head())

stock_df=pd.DataFrame()
for stocks in stock_list:
    data=yf.download(stocks,period=f'{years}y')
    stock_df[f'{stocks}']=data['Close']

# print("Stock DF Columns:", stock_df.columns)
# print("SP500 Columns:", SP500.columns)

# 1. SP500 mein se sirf 'Close' column rakhein aur use 'sp500' naam dein
SP500 = SP500[['Close']]
SP500.columns = ['sp500']

# 2. Dono DataFrames ka index reset karein taaki 'Date' column bahar aa jaye
stock_df = stock_df.reset_index()
SP500 = SP500.reset_index()

# 3. Ab check karein, kya dono mein 'Date' aa gaya?
# (Yfinance mein kabhi-kabhi column ka naam 'Date' hota hai, kabhi 'index')
# Safe side ke liye hum rename kar dete hain agar naam 'index' hai:
stock_df.rename(columns={'index': 'Date'}, inplace=True)
SP500.rename(columns={'index': 'Date'}, inplace=True)

# 4. Ab merge karein
stock_df = pd.merge(stock_df, SP500, on='Date', how='inner')

#Note:If you want to change the dtype use astype function
# print(stock_df.head())

col1,col2 =st.columns([1,1])
with col1:
    st.markdown("### DataFrame Head")
    st.dataframe(stock_df.head(),use_container_width=True)
with col2:
    st.markdown("### DataFrame Tail")
    st.dataframe(stock_df.tail(),use_container_width=True)

col1,col2=st.columns([1,1])
with col1:
    st.markdown("### Price of all the stocks ")
    st.plotly_chart(Capm_function.interactive_chart(stock_df))

with col2:
    st.markdown("### Price of all the stocks (After Normalizing)")
    st.plotly_chart(Capm_function.interactive_chart(Capm_function.normalize(stock_df)))

stock_daily_return=Capm_function.daily_returns(stock_df)
print(stock_daily_return.head())

# Do khali dictionaries banayein values store karne ke liye
beta = {}
alpha = {}

# Har column par loop chalayein
for i in stock_daily_return.columns:
    # Date aur Market (sp500) ko chhod kar baaki stocks ka calculation karein
    if i != 'Date' and i != 'sp500':
        # Beta aur Alpha calculate karne wala function call karein
        b, a = Capm_function.calculate_beta(stock_daily_return, i)

        # Results ko dictionaries mein save karein
        beta[i] = b
        alpha[i] = a

# Final results check karein
print(beta, alpha)

# 1. Beta values ka DataFrame banana
beta_df = pd.DataFrame(columns=['Stock', 'Beta Value'])
beta_df['Stock'] = beta.keys()
beta_df['Beta Value'] = [str(round(i, 2)) for i in beta.values()]

# 2. Streamlit mein Beta values display karna
with col1:
    st.markdown('### Calculated Beta Value')
    st.dataframe(beta_df, use_container_width=True)

# 3. CAPM Formula variables define karna
rf = 0  # Risk-free rate
rm = stock_daily_return['sp500'].mean() * 252  # Market Return

# 4. Expected Returns calculate karna (CAPM Formula)
return_df = pd.DataFrame()
return_value = []

for stock, value in beta.items():
    # CAPM Formula: ri = rf + Beta * (rm - rf)
    # Note: Screenshot mein (rf-rm) tha, standard formula (rm-rf) hota hai
    calc_return = rf + (value * (rm - rf))
    return_value.append(str(round(calc_return, 2)))

# 5. Return values ka DataFrame banana
return_df['Stock'] = beta.keys() # Ya stocks_list use karein
return_df['Return Value'] = return_value

with col2:
    st.markdown('### Calculated return using CAPM')
    st.dataframe(return_df,use_container_width=True)

