import streamlit as st
import pandas as pd

# Initialize the session state variables
if 'scores' not in st.session_state:
    st.session_state['scores'] = []

if 'title' not in st.session_state:
    st.session_state['title'] = "Top 5 Scores"

st.title("Admin Page - Update Scores")

# Section to change the title
st.header("Update Leaderboard Title")
new_title = st.text_input("Leaderboard Title", st.session_state['title'])
if st.button("Update Title"):
    st.session_state['title'] = new_title
    st.success(f"Updated title to: {new_title}")

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
