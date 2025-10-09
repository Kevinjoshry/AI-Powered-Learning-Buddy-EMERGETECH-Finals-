Technical Readme – AI-Powered Learning Buddy

SDG and Target:
Our project aligns with SDG 4: Quality Education, specifically targeting inclusive and equitable quality education. The AI Learning Buddy assists students by providing instant explanations, feedback, and study tips, helping learners overcome obstacles and improve comprehension, regardless of location or prior knowledge.

Tech Stack:

Backend: Python, FastAPI, Google Generative AI (Gemini model)

Frontend: Streamlit for interactive UI

Data Handling & Utilities: Pandas, NumPy, JSON

Deployment: Render (Backend) and Streamlit Cloud (Frontend)

Version Control & Collaboration: Git & GitHub

Architecture:

The frontend (Streamlit app) captures user inputs and maintains chat history.

User messages are sent as POST requests to the FastAPI backend endpoint /chat.

The backend combines chat history and the new message into a prompt, which is passed to the Google Gemini Generative AI model.

The AI model returns a response, which the backend sends back as JSON to the frontend.

Streamlit updates the chat interface in real-time, displaying the user query and AI response.

This architecture ensures seamless, real-time interaction while maintaining the history context for meaningful AI responses.

Biggest Challenge:
The most difficult technical hurdle was resolving dependency conflicts in the Python environment, especially around protobuf versions required by multiple Google AI libraries and grpcio-status. These conflicts prevented successful deployment of the backend initially. We overcame this by:

Reviewing library requirements carefully, identifying incompatible version constraints.

Loosening or removing specific version pins in requirements.txt to allow pip to resolve compatible versions automatically.

Testing locally in a virtual environment to ensure the backend runs as expected before deploying.

This solution allowed the backend to deploy smoothly on Render, enabling the frontend to connect without errors and deliver a responsive AI chat experience.