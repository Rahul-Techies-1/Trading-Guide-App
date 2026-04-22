import plotly.express as px
import numpy as np

def interactive_chart(df):
    fig=px.line()
    for i in df.columns[1:]:
        fig.add_scatter(x=df['Date'],y=df[i],name=i)
    fig.update_layout(width=450,margin=dict(l=20,t=50,r=20,b=20),legend=dict(orientation='h',yanchor='bottom',y=1.02,xanchor='right',x=1))
    return fig

# Function to normalize the price based on their initial price
def normalize(df_2):
    df=df_2.copy()
    for i in df.columns[1:]:
        df[i]=df[i]/df[i][0]
    return df

# Function to calculate daily returns
def daily_returns(df):
    df_daily_return = df.copy()
    for i in df.columns[1:]:
        df_daily_return[i] = df_daily_return[i].astype(float)

        for j in range(1, len(df)):
            df_daily_return[i][j] = ((df[i][j] - df[i][j - 1]) / df[i][j - 1]) * 100

        df_daily_return[i][0] = 0

    return df_daily_return


def calculate_beta(stock_daily_return, stock):
    # Market (S&P 500) ka average annual return nikalna
    # mean() * 252 (trading days in a year)
    rm = stock_daily_return['sp500'].mean() * 252

    # np.polyfit linear regression use karta hai (Degree 1 yaani straight line)
    # b = Beta (Slope), a = Alpha (Intercept)
    b, a = np.polyfit(stock_daily_return['sp500'], stock_daily_return[stock], 1)

    return b, a

