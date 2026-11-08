
import streamlit as st
import requests

# ====================================
# 1. APPLICATION CONFIGURATION
# ====================================

st.set_page_config(
    page_title="BhashaAI",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 BhashaAI")
st.subheader("Your Personal AI Learning Assistant")

st.write(
    "Ask me anything about Python, SQL, "
    "Machine Learning, GenAI and more!"
)

# ====================================
# 2. MODEL CONFIGURATION
# ====================================

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3.2:1b"

# ====================================
# 3. SYSTEM PROMPT
# ====================================

SYSTEM_PROMPT = """
You are BhashaAI, a helpful AI learning assistant.

Your responsibilities:
1. Explain concepts in simple language.
2. Give practical Python examples.
3. Help with SQL and Machine Learning.
4. Explain errors and their solutions.
5. Give real-world examples.

Keep answers clear and beginner-friendly.
"""

# ====================================
# 4. CHAT HISTORY
# ====================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ====================================
# 5. USER INPUT
# ====================================

user_input = st.chat_input("Ask your question...")

if user_input:

    # Display user question

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # ====================================
    # 6. PREPARE PROMPT
    # ====================================

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    messages.extend(st.session_state.messages)

    # ====================================
    # 7. CONNECT TO LLM
    # ====================================

    with st.chat_message("assistant"):

        with st.spinner("AI is thinking..."):

            try:

                response = requests.post(
                    OLLAMA_URL,
                    json={
                        "model": MODEL_NAME,
                        "messages": messages,
                        "stream": False
                    },
                    timeout=180
                )

                response.raise_for_status()

                result = response.json()

                ai_response = result["message"]["content"]

                st.markdown(ai_response)

                # Save AI response

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": ai_response
                })

            except requests.exceptions.ConnectionError:

                st.error(
                    "Cannot connect to Ollama. "
                    "Please start Ollama and try again."
                )

            except requests.exceptions.RequestException as error:

                st.error(f"Request error: {error}")

            except (KeyError, ValueError):

                st.error("Could not process the AI response.")
