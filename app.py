import streamlit as st
import pandas as pd

st.set_page_config(page_title="Random Quiz Generator", layout="wide")

st.title("🎯 Random Quiz Generator")

# Upload file
uploaded_file = st.file_uploader("Upload your Question Bank (CSV)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Settings
    total_questions = st.number_input("Total number of questions", min_value=1, max_value=100, value=10)
    col1, col2, col3 = st.columns(3)
    with col1:
        hard_pct = st.slider("Hard %", 0, 100, 20)
    with col2:
        medium_pct = st.slider("Medium %", 0, 100, 50)
    with col3:
        easy_pct = 100 - (hard_pct + medium_pct)
        st.metric("Easy %", easy_pct)

    if st.button("🎲 Generate Quiz"):
        # Calculate number of questions
        num_hard = int(total_questions * hard_pct / 100)
        num_medium = int(total_questions * medium_pct / 100)
        num_easy = total_questions - (num_hard + num_medium)

        # Sample questions
        hard_qs = df[df['difficulty'] == 'hard'].sample(num_hard, replace=False)
        medium_qs = df[df['difficulty'] == 'medium'].sample(num_medium, replace=False)
        easy_qs = df[df['difficulty'] == 'easy'].sample(num_easy, replace=False)

        quiz = pd.concat([hard_qs, medium_qs, easy_qs]).sample(frac=1).reset_index(drop=True)

        st.subheader("📋 Your Randomized Quiz")
        for i, row in quiz.iterrows():
            st.write(f"**Q{i+1}: {row['Question']}**")
            for opt in ['option_1', 'option_2', 'option_3', 'option_4', 'option_5']:
                if pd.notna(row[opt]):
                    st.write(f"- {row[opt]}")
