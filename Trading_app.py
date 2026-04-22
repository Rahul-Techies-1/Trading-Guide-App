import streamlit as st



st.markdown("""
    <style>
    /* 1. Main Title styling */
    .app-title {
        font-size: 45px !important;
        font-weight: 800;
        color: #1E3A8A; /* Deep Professional Blue */
        margin-bottom: 5px;
        font-family: 'Helvetica Neue', sans-serif;
    }

    /* 2. Tagline styling */
    .tagline {
        font-size: 24px !important;
        font-weight: 500;
        color: #4B5563; /* Subtle Dark Gray (mismatch nahi hoga) */
        line-height: 1.4;
        margin-top: -10px; /* Title ke paas lane ke liye */
        margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True)


st.set_page_config(page_title='Trading App',
                   page_icon='chart_with_downward_trend:',
                   layout='wide')
st.set_page_config(initial_sidebar_state="expanded")
# st.sidebar.success("Select a page above")
st.markdown('<p class="app-title">Trading Guide App 📊</p>', unsafe_allow_html=True)


st.markdown('<p class="tagline">We provide the Greatest Platform for you to collect all information prior to investing in stocks</p>', unsafe_allow_html=True)


col1, col2, col3 = st.columns([0.2, 0.3, 0.2]) # Beech wala 2x bada hai side walon se

with col2:
    st.image("app.avif", use_container_width=True)


st.markdown('<p class="big-font">We provide the following services:</p>', unsafe_allow_html=True)


st.markdown('<p class="service-title">1️⃣ Stock Information</p>', unsafe_allow_html=True)
st.markdown('<p class="service-desc">Through this page, you can see all the information about stock</p>', unsafe_allow_html=True)


st.markdown('<p class="service-title">2️⃣ Stock Prediction</p>', unsafe_allow_html=True)
st.markdown('<p class="service-desc">You can explore predicted closing prices for the next 30 days based on historical stock data and advanced forecasting models</p>', unsafe_allow_html=True)


st.markdown('<p class="service-title">3️⃣ CAPM Return</p>', unsafe_allow_html=True)
st.markdown('<p class="service-desc">Discover how the Capital Asset Pricing Model (CAPM) calculates the expected return of different stocks asset based on its risk</p>', unsafe_allow_html=True)


st.markdown('<p class="service-title">4️⃣ CAPM Beta</p>', unsafe_allow_html=True)
st.markdown('<p class="service-desc">Calculates Beta and Expected Return for Individual Stocks.</p>', unsafe_allow_html=True)