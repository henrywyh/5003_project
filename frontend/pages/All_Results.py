import streamlit as st
import requests
import time
import pandas as pd
from const import BACKEND_URL

st.set_page_config(page_title='Mental Health Analysis', page_icon=':bar_chart:', layout='wide')
# Listen to the Enter key when the submit button is focused


st.title('All Results')
def fetch_data():
    response = requests.get(f'{BACKEND_URL}/get_stream_result')
    if response.status_code == 200:
        return response.json()
    else:
        return None

table_placeholder = st.empty()
# Constantly pull the backend for new results 
# and replace the old  table with the new one
while True:
    with st.spinner('Pulling Any New Posts from reddit...'):
        data = fetch_data()
    # Update the table with the new data
    if data is not None:
        df = pd.DataFrame(data, columns=['Post title', 'Is Depressed'], )
        table_placeholder.table(df, )
    else:
        st.error('Failed to fetch data from the backend API.')

    # Wait for 5 seconds
    time.sleep(5)