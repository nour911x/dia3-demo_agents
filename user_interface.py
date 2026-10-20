import streamlit as st
from llm_agent import ConversationAgent


class UserInterface:
	def __init__(self):
		st.set_page_config(page_title="Jarvis")
		st.title("Barbe-Quasar")
		self.conversation_agent_object = self.get_persistant_conversation_agent()


	def get_persistant_conversation_agent(self):

		if "conversation_agent_object" not in st.session_state:
			st.session_state.conversation_agent_object = ConversationAgent()

		return st.session_state.conversation_agent_object


	def show_message_content(self, content):
		if isinstance(content, str):
			st.markdown(content)
		else:
			for part in content:
				if part["type"] == "text":
					st.markdown(part["text"])
				else:
					st.image(part["image_url"]["url"])


	def show_discussion_history(self):
		for message in self.conversation_agent_object.get_conversation_history():
			with st.chat_message(message["role"]):
				self.show_message_content(message["content"])


	def run(self):
		interaction = st.chat_input(
			"Que veux tu moussaillon ?",
			accept_file=True,
			file_type=["png", "jpg", "jpeg"],
			accept_audio=False
			)

		if interaction:
			image_file = None
			if interaction.files:
				image_file = interaction.files[0]

			self.conversation_agent_object.ask_llm(interaction.text, image_file)
			self.show_discussion_history()


if __name__ == "__main__":
	user_interface_object = UserInterface()
	user_interface_object.run()
