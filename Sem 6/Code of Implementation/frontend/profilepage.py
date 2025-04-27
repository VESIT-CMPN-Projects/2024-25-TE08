import streamlit as st
import time

# Fetch user email from session state
if 'user' in st.session_state:
    user_email = st.session_state['user']['email']
else:
    st.warning("You need to log in to view your profile.")
    st.stop()

# Extract username from email (before @)
default_username = user_email.split('@')[0] if user_email else "User"

# Use extracted username if no custom username is set
display_name = st.session_state.get('username', default_username)

# Set title
title = f"Hello, {display_name}!"
st.title(title)

email_icon = ':material/mail:'
st.write(f"{email_icon} Email: {user_email}")

# Input for username
username = st.text_input("Username", placeholder="Enter your username", value='')

# Button to save or edit username
if st.button("Save Username"):
    if username:
        st.session_state['username'] = username  # Store username in session state
        st.success(f"Username '{username}' saved successfully!")
        time.sleep(1)
        st.rerun()  # Rerun the page to show updated username
    else:
        st.warning("Please enter a username.")

# Logout button
if st.button("Logout"):
    # Clear user session and redirect to login page
    del st.session_state['user']
    st.session_state.pop('username', None)  # Clear stored username
    st.session_state['logged_out'] = True
    st.success("Logged out successfully!")
    time.sleep(1)
    st.rerun()  # Redirect to login page
