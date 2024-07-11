import streamlit as st

import gspread
import pandas as pd

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
username_password_worksheet = user_data_parent_sheet.worksheet("Username_Password")
username_password_worksheet_df = pd.DataFrame(username_password_worksheet.get_all_records())

def signup_user_button_clicked(new_first_name, new_last_name, new_user_name, new_email_address, new_password):
    if new_email_address not in username_password_worksheet_df['Email Address'].to_list():
        st.success('User signed up successfully. Proceeding to login page...')
        user_data_parent_sheet.add_worksheet(title=new_user_name, rows=1000, cols=26)
        username_password_worksheet.update_cell(username_password_worksheet_df.shape[0]+2, 1, new_first_name)
        username_password_worksheet.update_cell(username_password_worksheet_df.shape[0]+2, 2, new_last_name)
        username_password_worksheet.update_cell(username_password_worksheet_df.shape[0]+2, 3, new_user_name)
        username_password_worksheet.update_cell(username_password_worksheet_df.shape[0]+2, 4, new_password)
        username_password_worksheet.update_cell(username_password_worksheet_df.shape[0]+2, 5, new_email_address)
    else:
        st.error('This email address is already registered. Please try logging in.')
    st.session_state.page='login'

def signup():
    
    st.title('Signup Page')
    new_first_name = st.text_input('First Name', key='signupfirstname', placeholder='First Name')
    new_last_name = st.text_input('Last Name', key='signuplastname', placeholder='Last Name')
    new_email_address = st.text_input('Email Address', key='signupemailaddress' , placeholder="someone@example.com")

    new_user_name = st.text_input('Username', key='signupusername' , value="".join((new_first_name+new_last_name).lower().strip().split()))
    if new_user_name in username_password_worksheet_df['Username'].to_list():
        st.error('Username already taken, try another one')
        
    new_password = st.text_input('Password', key='signuppassword', type='password', placeholder='Password')
    confirm_new_password = st.text_input('Confirm New Password', key='signupconfirmpassword', placeholder='Confirm Password')
    if new_password==confirm_new_password and len(new_password)!=0:
        st.success('Passwords match. Proceed to Sign Up')
    elif len(new_password)!=0 and new_password!=confirm_new_password:
        st.error("Passwords don't match") 

    st.button('Signup', on_click=signup_user_button_clicked, args=(new_first_name, new_last_name, new_user_name, new_email_address, new_password))