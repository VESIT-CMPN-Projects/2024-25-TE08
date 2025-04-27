import streamlit as st

def clear_user_input():
    """Clears only the user-entered topic text or uploaded PDF."""
    keys_to_clear = ["user_topic", "user_input", "uploaded_file"]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
