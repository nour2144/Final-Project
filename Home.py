import pandas as pd
import streamlit as st
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
import time
import numpy as np
pages = ['Home','Predict','Plotting']
df = pd.read_csv('Cleaned_baku_housing.csv',index_col='Unnamed: 0')
# model = joblib.load("model.pkl")
st.set_page_config(page_title='Betta Ai', page_icon='📈', layout="wide", initial_sidebar_state="collapsed")
st.logo('images/logo.png', icon_image='images/neww.png')
st.sidebar.title("Hi There!",)
st.sidebar.markdown("Take a look in my website :shark:")
welcome_message = """
Welcome to our AI-powered platform for predicting home prices!
We're here to help you make informed investment decisions. With our advanced artificial intelligence technology, we provide accurate and up-to-date predictions for home prices. Start now and discover how our AI can help you achieve your real estate goals with confidence and ease.


"""  

def stream_data():
    time.sleep(2)
    for word in welcome_message.split(" "):
        yield word + " "
        time.sleep(0.02)
    st.image("images/ml.png", caption="Sunrise Of AI")
    st.title('OUR DATASET')

    yield df.head(7)

st.write_stream(stream_data)


