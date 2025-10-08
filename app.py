import streamlit as st
import pandas as pd
import joblib

# -----------------------------
# LOAD DATA AND MODEL
# -----------------------------
@st.cache_data
def load_questions():
    return pd.read_csv("questions.csv")

@st.cache_resource
def load_model():
    model = joblib.load("model.pkl")
    labels = joblib.load("labels.pkl")
    return model, labels

questions = load_questions()
model, labels = load_model()

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="AI Learning Buddy", page_icon="🤖", layout="centered")

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "title"

# -----------------------------
# TITLE PAGE (Styled)
# -----------------------------
def title_page():
    st.markdown(
        """
        <style>
        body {
            background: linear-gradient(135deg, #1d3557, #457b9d);
            color: white;
        }
        .main {
            background: none;
        }
        .title-container {
            text-align: center;
            margin-top: 150px;
            padding: 60px;
            border-radius: 20px;
            background: rgba(255, 255, 255, 0.1);
            box-shadow: 0px 0px 30px rgba(255, 255, 255, 0.2);
        }
        h1 {
            font-size: 60px;
            color: #f1faee;
            text-shadow: 2px 2px 20px #a8dadc;
        }
        p {
            font-size: 18px;
            color: #f1faee;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="title-container">
            <h1>🤖 AI-Powered Learning Buddy</h1>
            <p>
                Welcome to your <b>AI Learning Companion</b>!<br><br>
                This smart assistant uses <b>Artificial Intelligence</b> to analyze your quiz performance 
                and provide <b>personalized study recommendations</b>.<br><br>
                Built for <b>EMERGETECH Finals</b> to promote <b>SDG 4: Quality Education</b>.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        "<div style='text-align:center;'>",
        unsafe_allow_html=True
    )
    if st.button("🚀 Start Quiz", use_container_width=False):
        st.session_state.page = "quiz"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# QUIZ PAGE
# -----------------------------
def quiz_page():
    st.markdown("<h1 style='text-align:center; color:#1d3557;'>🧩 Take the Quiz</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Answer all questions below to get your AI feedback.</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Presented by: Rasco, Jeramieh | Anunciacion, Klein | Santos, Kevin Josh</p>", unsafe_allow_html=True)

    score = 0
    user_answers = []
    total_questions = len(questions)

    for i, row in questions.iterrows():
        st.subheader(f"Question {i+1}/{total_questions}")
        st.write(f"**{row['question']}**")

        options = [row['optionA'], row['optionB'], row['optionC'], row['optionD']]
        user_choice = st.radio("Select your answer:", options, key=f"q{i}")
        user_answers.append(user_choice)

        st.progress((i + 1) / total_questions)
        st.markdown("---")

    if st.button("🧠 Evaluate My Learning"):
        for i, row in questions.iterrows():
            if user_answers[i] == row['answer']:
                score += 1

        total = len(questions)
        pct_score = (score / total) * 100

        st.markdown("---")
        st.markdown("<h2 style='text-align:center;'>📊 Your Results</h2>", unsafe_allow_html=True)

        if pct_score < 50:
            st.error(f"Your Score: {score}/{total} ({pct_score:.1f}%) 😟")
        elif pct_score < 80:
            st.warning(f"Your Score: {score}/{total} ({pct_score:.1f}%) 🙂")
        else:
            st.success(f"Your Score: {score}/{total} ({pct_score:.1f}%) 🎉")

        # AI recommendation
        time_per_question = 8
        difficulty = "medium"
        difficulty_code = {"easy": 0, "medium": 1, "hard": 2}[difficulty]

        pred = model.predict([[pct_score, time_per_question, difficulty_code]])[0]
        recommendation = labels[pred]

        st.markdown("<h2 style='text-align:center;'>🧠 AI Recommendation</h2>", unsafe_allow_html=True)

        if recommendation == "review":
            st.warning("🔁 The AI suggests you **review the basics** before moving forward.")
        elif recommendation == "practice":
            st.info("💪 The AI recommends you **keep practicing** — you're improving fast!")
        else:
            st.success("🚀 Excellent work! The AI says you're ready to **advance** to harder topics!")

        st.markdown("---")

        if st.button("🔄 Back to Title Page"):
            st.session_state.page = "title"
            st.rerun()

    st.caption("AI-Powered Learning Buddy © 2025 | Built with ❤️ for EMERGETECH Finals")

# -----------------------------
# PAGE ROUTER
# -----------------------------
if st.session_state.page == "title":
    title_page()
elif st.session_state.page == "quiz":
    quiz_page()
