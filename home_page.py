import streamlit as st

def logout_user_button_clicked():
    st.session_state.logged_in = False
    st.session_state.page = 'login'
    st.error('User logged out successfully. Re-login to continue...')

def home():
    st.title('Home Page')
    st.button('Logout', on_click=logout_user_button_clicked)