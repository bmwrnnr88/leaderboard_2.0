import streamlit as st
import pandas as pd
from collections import defaultdict

# Initialize a list to store student scores
if 'scores' not in st.session_state:
    st.session_state['scores'] = []

st.title("Mr. Ward's Final Exam Leaderboard")

# Input section
st.header("Enter New Score")
name = st.text_input("Student Name")
score = st.number_input("Score", min_value=0, max_value=100, step=1)

if st.button("Add Score"):
    if name and score is not None:
        st.session_state['scores'].append({'name': name, 'score': score})
        st.success(f"Added {name} with score {score}")
    else:
        st.error("Please enter both name and score")

# Data processing
df = pd.DataFrame(st.session_state['scores'])

# Sorting and selecting top 5 scores
if not df.empty:
    df = df.sort_values(by='score', ascending=False)
    top_scores = df.groupby('score').head(1).head(5)['score'].tolist()
    df = df[df['score'].isin(top_scores)]

# Display leaderboard with differentiation
st.header("Top 5 Scores")
if not df.empty:
    def get_medal(idx):
        if idx == 0:
            return "🥇"
        elif idx == 1:
            return "🥈"
        elif idx == 2:
            return "🥉"
        else:
            return ""

    # Group by scores
    grouped = df.groupby('score')['name'].apply(list).reset_index()

    # Generate the leaderboard HTML
    leaderboard_html = "<table style='width:100%; border-collapse: collapse;'>"
    leaderboard_html += "<tr><th style='text-align: left;'>Rank</th><th style='text-align: left;'>Names</th><th style='text-align: left;'>Score</th></tr>"
    
    for idx, row in grouped.iterrows():
        medal = get_medal(idx)
        color = "gold" if idx == 0 else "silver" if idx == 1 else "bronze" if idx == 2 else "white"
        names = ", ".join(row['name'])
        leaderboard_html += f"<tr style='background-color: {color};'><td>{medal}</td><td>{names}</td><td>{row['score']}</td></tr>"
    
    leaderboard_html += "</table>"
    st.markdown(leaderboard_html, unsafe_allow_html=True)
else:
    st.write("No scores available yet.")

# Option to clear scores
if st.button("Clear All Scores"):
    st.session_state['scores'] = []
    st.success("Cleared all scores")
