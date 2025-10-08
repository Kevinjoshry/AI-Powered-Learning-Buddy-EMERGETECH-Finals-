import streamlit as st
import requests

BACKEND_URL = "https://ai-powered-learning-buddy-emergetech.onrender.com"  # update if deployed

def chatbot_page():
    st.markdown(
        """
        <h1 style='text-align:center; color:#1d3557;'>💬 Ask Your AI Learning Buddy</h1>
        <p style='text-align:center;'>Get instant feedback, explanations, or tips from your AI assistant.</p>
        """, unsafe_allow_html=True
    )

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history
    for chat in st.session_state.chat_history:
        role = chat["role"]
        content = chat["content"]
        if role == "user":
            st.markdown(f"<div style='text-align:right; background:#a8dadc; color:#1d3557; padding:10px; border-radius:10px; margin:5px 0;'>{content}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align:left; background:#f1faee; color:#1d3557; padding:10px; border-radius:10px; margin:5px 0;'>{content}</div>", unsafe_allow_html=True)

    # Input field
    user_message = st.text_input("Type your message:", key="user_input")

    if st.button("Send 💬"):
        if user_message.strip():
            st.session_state.chat_history.append({"role": "user", "content": user_message})

            try:
                response = requests.post(
                    BACKEND_URL,
                    json={
                        "message": user_message,
                        "history": st.session_state.chat_history
                    },
                    timeout=30
                )

                if response.status_code == 200:
                    bot_reply = response.json().get("reply", "No reply from AI.")
                    st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
                else:
                    st.session_state.chat_history.append({"role": "assistant", "content": f"Error: {response.status_code}"})

            except Exception as e:
                st.session_state.chat_history.append({"role": "assistant", "content": f"⚠️ Connection error: {e}"})

            st.rerun()

    if st.button("🔄 Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

    st.caption("Gemini Chatbot © 2025 | Built with ❤️ for EMERGETECH Finals")
