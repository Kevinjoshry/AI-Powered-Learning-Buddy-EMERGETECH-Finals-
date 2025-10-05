import streamlit as st
import pandas as pd
import joblib

# -----------------------------
# LOAD DATA AND MODEL
# -----------------------------
@st.cache_data
def load_questions():
    # Example structure: question, optionA, optionB, optionC, optionD, answer
    return pd.read_csv("questions.csv")

@st.cache_resource
def load_model():
    model = joblib.load("model.pkl")
    labels = joblib.load("labels.pkl")
    return model, labels

questions = load_questions()
model, labels = load_model()

# -----------------------------
# STREAMLIT APP UI
# -----------------------------
st.set_page_config(page_title="AI Learning Buddy", page_icon="🤖", layout="centered")

st.title("🤖 AI-Powered Learning Buddy")
st.write("Welcome! Answer a few questions below and see how our AI evaluates your performance.")

score = 0
user_answers = []

# Display each question
for i, row in questions.iterrows():
    st.subheader(f"Q{i+1}: {row['question']}")
    options = [row['optionA'], row['optionB'], row['optionC'], row['optionD']]
    answer = st.radio("Choose an answer:", options, key=f"q{i}")

    user_answers.append(answer)
    if answer == row['answer']:
        score += 1

# -----------------------------
# EVALUATION & AI RECOMMENDATION
# -----------------------------
if st.button("Show Results"):
    total = len(questions)
    pct_score = (score / total) * 100

    st.markdown("---")
    st.header("📊 Results")
    st.write(f"**Your Score:** {score}/{total} ({pct_score:.1f}%)")

    # Simulated extra data (you can later make these dynamic)
    time_per_question = 8  # seconds (average)
    difficulty = "medium"  # assumed quiz level

    # Convert difficulty to numeric code
    difficulty_code = {"easy": 0, "medium": 1, "hard": 2}[difficulty]

    # Make AI prediction
    pred = model.predict([[pct_score, time_per_question, difficulty_code]])[0]
    recommendation = labels[pred]

    # -----------------------------
    # DISPLAY AI RECOMMENDATION
    # -----------------------------
    st.markdown("---")
    st.header("🧠 AI Recommendation")

    if recommendation == "review":
        st.warning("You should **review the basics** before moving on.")
        st.write("Try revisiting foundational topics to strengthen your understanding.")
    elif recommendation == "practice":
        st.info("You're doing well! Keep **practicing** to improve your confidence.")
        st.write("You’re almost there — consistency is key!")
    else:
        st.success("Excellent work! You’re ready to **advance** to harder topics.")
        st.write("The AI suggests moving on to more challenging exercises.")

    st.markdown("---")
    st.caption("AI-Powered Learning Buddy © 2025 | Built with ❤️ for EMERGETECH Finals")
