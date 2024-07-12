import streamlit as st

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import urllib.parse

username = urllib.parse.quote_plus(st.secrets.MONGO_DB_USERNAME)
password = urllib.parse.quote_plus(st.secrets.MONGO_DB_PASSWORD)

client = MongoClient(f'mongodb+srv://{username}:{password}@my-cluster.k0gdeoi.mongodb.net/?retryWrites=true&w=majority&appName=my-cluster', server_api=ServerApi('1'))
database = client[st.secrets.MONGO_DB_DBNAME]
collection = database[st.secrets.MONGO_DB_COLLECTION_NAME]

def login_user_button_clicked(username, password):
    
    if collection.count_documents({'username':username})!=0:
        if collection.find_one({'username':username})['password'] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("User logged in Successfully.")
        else:
            st.error('Invalid Credentials')
    else:
        st.error('User not registered! Sign Up to continue...')
        st.session_state.page = 'signup'

def login_to_signup_nav_button_clicked():
    st.session_state.page = 'signup'

def login():
    st.title('Login Page')
    username = st.text_input('Username', key = 'login_username', placeholder='Username')
    password = st.text_input('Password', type='password', key='login_password', placeholder='Password')

    col1, col2 = st.columns([1,1])
    with col1:
        st.button('Login', use_container_width=True, on_click=login_user_button_clicked, args=(username, password))       
    with col2:
        st.button('Sign Up', use_container_width=True, on_click=login_to_signup_nav_button_clicked)