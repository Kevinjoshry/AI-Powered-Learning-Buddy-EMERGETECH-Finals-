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

# -----------------------------
# INITIALIZE SESSION STATE
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "title"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = [None] * len(questions)

# -----------------------------
# TITLE PAGE
# -----------------------------
def title_page():
    st.markdown(
        """
        <h1 style='text-align:center; color:#f1faee;'>🤖 AI-Powered Learning Buddy</h1>
        <p style='text-align:center; color:#f1faee;'>Your AI companion for personalized learning.</p>
        """,
        unsafe_allow_html=True
    )
    
left, center, right = st.columns([1, 2, 1])

    with center:
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🚀 Start Quiz", key="start_quiz"):
                st.session_state.page = "quiz"
                st.rerun()
        with c2:
            if st.button("💬 Go to Chatbot", key="go_chatbot"):
                st.session_state.page = "chatbot"
                st.rerun()
                
# -----------------------------
# QUIZ PAGE
# -----------------------------
def quiz_page():
    st.markdown("<h1 style='text-align:center; color:#1d3557;'>🧩 Take the Quiz</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Answer all questions below to get your AI feedback.</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Presented By: Rasco, Jeramieh | Anunciacion, Klein | Santos, Kevin Josh</p>", unsafe_allow_html=True)

    score = 0

    # Render questions
    for i, row in questions.iterrows():
        st.subheader(f"Question {i+1}/{len(questions)}")
        st.write(f"**{row['question']}**")

        options = [row['optionA'], row['optionB'], row['optionC'], row['optionD']]
        # Use session state to persist answers
        st.session_state.quiz_answers[i] = st.radio(
            "Select your answer:", 
            options, 
            index=options.index(st.session_state.quiz_answers[i]) if st.session_state.quiz_answers[i] in options else 0,
            key=f"q{i}"
        )

    if st.button("🧠 Evaluate My Learning", key="eval_quiz"):
        # Calculate score
        for i, row in questions.iterrows():
            if st.session_state.quiz_answers[i] == row['answer']:
                score += 1

        total = len(questions)
        pct_score = (score / total) * 100
        st.markdown(f"**Your Score:** {score}/{total} ({pct_score:.1f}%)")

        # AI Recommendation
        # Optional: Use a simple rule-based logic or ML model
        wrong_questions = [i for i, row in enumerate(questions.iterrows()) if st.session_state.quiz_answers[i] != row[1]['answer']]
        avg_wrong_difficulty = (sum(questions.loc[i, "difficulty"] for i in wrong_questions) / len(wrong_questions)) if wrong_questions else 1

        # Example logic
        if pct_score < 50:
            recommendation = "review"
        elif pct_score < 80:
            recommendation = "practice"
        else:
            recommendation = "advance"

        if recommendation == "review":
            st.warning("🔁 The AI suggests you review the basics before moving forward.")
        elif recommendation == "practice":
            st.info("💪 The AI recommends you keep practicing — you're improving fast!")
        else:
            st.success("🚀 Excellent work! The AI says you're ready to advance to harder topics!")

    if st.button("🔄 Back to Title Page", key="back_from_quiz"):
        st.session_state.page = "title"
        st.rerun()

# -----------------------------
# CHATBOT PAGE
# -----------------------------
def chatbot_page():
    st.markdown("<h1 style='text-align:center; color:#1d3557;'>💬 AI Learning Buddy Chatbot</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Ask me anything about the quiz topics!</p>", unsafe_allow_html=True)

    # Display chat history
    for sender, msg in st.session_state.chat_history:
        if sender == "You":
            st.markdown(f"**You:** {msg}")
        else:
            st.markdown(f"**AI:** {msg}")

    st.markdown("---")

    # Input
    user_input = st.text_input("Your question:", st.session_state.user_input, key="chat_input")

    if st.button("Send", key="send_chat") and user_input.strip():
        # Save input
        user_question = user_input
        st.session_state.user_input = ""  # Clear input

        # Simple rule-based AI
        q_lower = user_question.lower()
        if "planet" in q_lower:
            response = "Mars is known as the Red Planet."
        elif "capital" in q_lower:
            response = "The capital of France is Paris."
        elif "color" in q_lower:
            response = "Red and blue make purple."
        elif "square root" in q_lower:
            response = "The square root of a number x is the number which, when multiplied by itself, gives x."
        else:
            response = "Hmm, I suggest reviewing your notes or trying a search online."

        st.session_state.chat_history.append(("You", user_question))
        st.session_state.chat_history.append(("AI", response))

    if st.button("🔄 Back to Title Page", key="back_from_chat"):
        st.session_state.page = "title"
        st.rerun()

# -----------------------------
# PAGE ROUTER
# -----------------------------
page = st.sidebar.radio(
    "Navigate",
    ["🏠 Title Page", "🧩 Quiz", "💬 Chatbot"],
    index=["🏠 Title Page", "🧩 Quiz", "💬 Chatbot"].index(
        {"title": "🏠 Title Page", "quiz": "🧩 Quiz", "chatbot": "💬 Chatbot"}[st.session_state.page]
        if st.session_state.page in ["title", "quiz", "chatbot"] else "🏠 Title Page"
    )
)

if page == "🏠 Title Page":
    title_page()
elif page == "🧩 Quiz":
    quiz_page()
elif page == "💬 Chatbot":
    from chatbot_page import chatbot_page
    chatbot_page()
