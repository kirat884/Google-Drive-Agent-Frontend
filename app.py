# frontend.py

import requests
import streamlit as st


BACKEND_URL = "https://google-drive-agent-backend.onrender.com/chat"


st.set_page_config(
    page_title="Google Drive AI Assistant",
    page_icon="📁",
    layout="centered"
)


st.title("📁 Google Drive AI Assistant")
st.caption("Ask me to search files from your Google Drive.")


if "messages" not in st.session_state:
    st.session_state.messages = []


with st.sidebar:
    st.header("Try these examples")

    examples = [
        "Find PDF files",
        "Is there any invoice file in the drive?",
        "Find files named resume",
        "Find Google Sheets about budget",
        "Find recent files",
        "Find files with word project",
    ]

    for example in examples:
        if st.button(example):
            st.session_state.pending_message = example

    st.divider()

    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()


# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Get input from example button or chat box
user_input = None

if "pending_message" in st.session_state:
    user_input = st.session_state.pending_message
    del st.session_state.pending_message
else:
    user_input = st.chat_input("Ask about your Drive files...")


if user_input:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Searching your Google Drive..."):
            try:
                response = requests.post(
                    BACKEND_URL,
                    json={
                        "message": user_input
                    },
                    timeout=60
                )

                if response.status_code == 200:
                    data = response.json()
                    bot_reply = data.get("response", "No response received.")
                else:
                    bot_reply = (
                        f"Backend error: {response.status_code}\n\n"
                        f"Details:\n```json\n{response.text}\n```"
                    )

            except requests.exceptions.ConnectionError:
                bot_reply = (
                    "Could not connect to backend.\n\n"
                    "Make sure FastAPI is running:\n\n"
                    "```bash\nuvicorn main:app --reload\n```"
                )

            except Exception as e:
                bot_reply = f"Something went wrong: {str(e)}"

        st.markdown(bot_reply)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": bot_reply
        }
    )