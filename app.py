import streamlit as st
import pandas as pd

# Initialize a list to store student scores
if 'scores' not in st.session_state:
    st.session_state['scores'] = []

# Custom CSS for larger fonts
st.markdown("""
    <style>
        .leaderboard-title {
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .leaderboard-table th, .leaderboard-table td {
            font-size: 24px;
            padding: 8px;
        }
        .medal {
            font-size: 24px; /* Adjust the font size for medal icons */
        }
        .rank-number {
            font-size: 24px; /* Adjust the font size for rank numbers */
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)

st.title("Mr. Ward's Final Exam Leaderboard")

# Input section
st.header("Enter New Score")
name = st.text_input("Student Name")
score = st.number_input("Score", min_value=0.0, max_value=100.0, step=0.1, format="%.1f")

if st.button("Add Score"):
    if name and score is not None:
        st.session_state['scores'].append({'name': name, 'score': round(score, 1)})
        st.success(f"Added {name} with score {score}")
    else:
        st.error("Please enter both name and score")

# Data processing
df = pd.DataFrame(st.session_state['scores'])

# Sorting and selecting top 5 scores
if not df.empty:
    # Sort by score in descending order
    df = df.sort_values(by='score', ascending=False)
    
    # Select top 5 unique scores
    top_scores = df['score'].unique()[:5]
    
    # Filter the dataframe to include only the top 5 scores
    df = df[df['score'].isin(top_scores)]

# Display leaderboard with differentiation
st.markdown("<div class='leaderboard-title'>Top 5 Scores</div>", unsafe_allow_html=True)
if not df.empty:
    def get_rank_marker(idx):
        if idx == 0:
            return "<span class='medal'>🥇</span>"
        elif idx == 1:
            return "<span class='medal'>🥈</span>"
        elif idx == 2:
            return "<span class='medal'>🥉</span>"
        elif idx == 3:
            return "<span class='rank-number'>4</span>"
        elif idx == 4:
            return "<span class='rank-number'>5</span>"
        else:
            return ""

    # Group by scores
    grouped = df.groupby('score')['name'].apply(list).reset_index()
    
    # Sort the grouped dataframe by score in descending order again
    grouped = grouped.sort_values(by='score', ascending=False).reset_index(drop=True)

    # Generate the leaderboard HTML
    leaderboard_html = "<table class='leaderboard-table' style='width:100%; border-collapse: collapse;'>"
    leaderboard_html += "<tr><th style='text-align: left;'>Rank</th><th style='text-align: left;'>Names</th><th style='text-align: left;'>Score</th></tr>"
    
    for idx, row in grouped.iterrows():
        rank_marker = get_rank_marker(idx)
        color = "gold" if idx == 0 else "silver" if idx == 1 else "bronze" if idx == 2 else "white"
        names = ", ".join(row['name'])
        leaderboard_html += f"<tr style='background-color: {color};'><td>{rank_marker}</td><td>{names}</td><td>{row['score']:.1f}</td></tr>"
    
    leaderboard_html += "</table>"
    st.markdown(leaderboard_html, unsafe_allow_html=True)
else:
    st.write("No scores available yet.")

# Option to clear scores
if st.button("Clear All Scores"):
    st.session_state['scores'] = []
    st.success("Cleared all scores")
