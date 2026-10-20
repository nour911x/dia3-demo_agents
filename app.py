import streamlit as st
from llm_agent import ConversationAgent


class ChatApp:
    def __init__(self):
        st.set_page_config(page_title="Jarvis")
        st.title("Barbe-Quasar")

        if "agent" not in st.session_state:
            st.session_state.agent = ConversationAgent()

        self.agent = st.session_state.agent

    def display_history(self):
        for message in self.agent.conversation_history[1:]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    def run(self):
        self.display_history()

        user_input = st.chat_input(
            "Que veux tu moussaillon ?",
            accept_file=False,
            accept_audio=False
        )

        if user_input:
            with st.chat_message("user"):
                st.markdown(user_input)

            response = self.agent.ask_llm(user_input)

            with st.chat_message("assistant"):
                st.markdown(response)


if __name__ == "__main__":
    app = ChatApp()
    app.run()
