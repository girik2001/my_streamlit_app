import streamlit as st
import gspread

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import urllib.parse

username = urllib.parse.quote_plus(st.secrets.MONGO_DB_USERNAME)
password = urllib.parse.quote_plus(st.secrets.MONGO_DB_PASSWORD)

client = MongoClient(f'mongodb+srv://{username}:{password}@my-cluster.k0gdeoi.mongodb.net/?retryWrites=true&w=majority&appName=my-cluster', server_api=ServerApi('1'))
database = client[st.secrets.MONGO_DB_DBNAME]
collection = database[st.secrets.MONGO_DB_COLLECTION_NAME]

USER_DATA_SHEETS_SERVICE_ACCOUNT_CREDS = {
    "type": st.secrets.type,
    "project_id": st.secrets.project_id,
    "private_key_id": st.secrets.private_key_id,
    "private_key": st.secrets.private_key,
    "client_email": st.secrets.client_email,
    "client_id": st.secrets.client_id,
    "auth_uri": st.secrets.auth_uri,
    "token_uri": st.secrets.token_uri,
    "auth_provider_x509_cert_url": st.secrets.auth_provider_x509_cert_url,
    "client_x509_cert_url": st.secrets.client_x509_cert_url,
    "universe_domain": st.secrets.universe_domain
}

gc = gspread.service_account_from_dict(USER_DATA_SHEETS_SERVICE_ACCOUNT_CREDS)
user_data_parent_sheet = gc.open_by_key(st.secrets.USER_DATA_SHEETS_ID)

def signup_user_button_clicked(new_first_name, new_last_name, new_user_name, new_email_address, new_password):
    if collection.count_documents({'email' : new_email_address}) == 0:
        print(collection.insert_one({
            '_id' : collection.count_documents({})+1,
            'firstname' : new_first_name,
            'lastname' : new_last_name,
            'username' : new_user_name,
            'password' : new_password,  
            'email' : new_email_address,
        }))
        user_data_parent_sheet.add_worksheet(title=new_user_name, rows=1000, cols=26)
        st.success('User signed up successfully. Proceeding to login page...')
    else:
        st.error('This email address is already registered. Please try logging in.')
    st.session_state.page='login'

def signup():
    
    st.title('Signup Page')
    new_first_name = st.text_input('First Name', key='signupfirstname', placeholder='First Name')
    new_last_name = st.text_input('Last Name', key='signuplastname', placeholder='Last Name')
    new_email_address = st.text_input('Email Address', key='signupemailaddress' , placeholder="someone@example.com")

    new_user_name = st.text_input('Username', key='signupusername' , value="".join((new_first_name+new_last_name).lower().strip().split()))
    
    if collection.count_documents({'username':new_user_name}):
        st.error('Username already taken, try another one')
        
    new_password = st.text_input('Password', key='signuppassword', type='password', placeholder='Password')
    confirm_new_password = st.text_input('Confirm New Password', key='signupconfirmpassword', placeholder='Confirm Password')
    if new_password==confirm_new_password and len(new_password)!=0:
        st.success('Passwords match. Proceed to Sign Up')
    elif len(new_password)!=0 and new_password!=confirm_new_password:
        st.error("Passwords don't match") 

    st.button('Signup', on_click=signup_user_button_clicked, args=(new_first_name, new_last_name, new_user_name, new_email_address, new_password))