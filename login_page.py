import streamlit as st
import pandas as pd

def login_user_button_clicked(username, password):
    user_data_sheets_url = f"https://docs.google.com/spreadsheets/d/{st.secrets.USER_DATA_SHEETS_ID}/edit#gid=0".replace('/edit#gid=', '/export?format=csv&gid=')
    username_pass_df = pd.read_csv(user_data_sheets_url)
    if username in username_pass_df['Username'].to_list():
        if str(username_pass_df['Password'][username_pass_df['Username'][username_pass_df['Username']==username.strip()].index[0]]) == str(password):
            st.session_state.logged_in = True
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