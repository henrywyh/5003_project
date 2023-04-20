import streamlit as st
import requests
from const import BACKEND_URL
st.set_page_config(page_title='Mental Health Analysis', page_icon=':bar_chart:', layout='wide')
# Listen to the Enter key when the submit button is focused

st.title('Mental Health Analysis')
with st.form('my_form'):
    text =st.text_area('Enter the text to be analyzed')
    submit = st.form_submit_button('Submit',use_container_width=True,)
    
    
if submit:
    # call the backend
    with st.spinner('Analyzing...'):
        response = requests.post(f'{BACKEND_URL}/depressed', json={'text': text}).json()
        if response == 1.0: 
            st.success('it is depression')
        else:
            st.success('it is not depression')
                