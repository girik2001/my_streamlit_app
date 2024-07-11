##### Importing Libraries
import streamlit as st
from login_page import login
from signup_page import signup
from home_page import home

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'page' not in st.session_state:
    st.session_state.page = 'login'

if not st.session_state.logged_in:
    if st.session_state.page == 'login':
        login()
    elif st.session_state.page == 'signup':
        signup()

if st.session_state.logged_in:
    home()