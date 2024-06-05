import streamlit as st
import pandas as pd

# Initialize a list to store student scores if it doesn't exist
if 'scores' not in st.session_state:
    st.session_state['scores'] = []

st.title("Admin Page - Update Scores")

st.header("Enter New Score")
name = st.text_input("Student Name")
score = st.number_input("Score", min_value=0.0, max_value=100.0, step=0.1, format="%.1f")

if st.button("Add Score"):
    if name and score is not None:
        st.session_state['scores'].append({'name': name, 'score': round(score, 1)})
        st.success(f"Added {name} with score {score}")
    else:
        st.error("Please enter both name and score")

# Option to clear scores
if st.button("Clear All Scores"):
    st.session_state['scores'] = []
    st.success("Cleared all scores")
