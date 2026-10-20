from groq import Groq

from dotenv import load_dotenv
import os
import base64


class ConversationAgent:
    def __init__(self):
        load_dotenv()
        self.groq_client = Groq(api_key=os.environ["GROQ_KEY"])
        self.conversation_history = [
                {
                    "role": "system",
                    "content": self.read_file(file_path="./context.txt")
                }
            ]


    @staticmethod
    def read_file(file_path):
        with open(file_path, "r") as file:
            return file.read()


    @staticmethod
    def encode_image(image_file):
        return base64.b64encode(image_file.read()).decode("utf-8")


    def get_conversation_history(self):
        return self.conversation_history[1: ]


    def update_conversation_history(self, role, content):
        self.conversation_history.append(
            {
            "role": role,
            "content": content,
            }
        )


    def ask_llm(self, text_interaction, image_file=None):

        if image_file:
            content = [
                {"type": "text", "text": text_interaction},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{self.encode_image(image_file)}"
                    }
                }
            ]
        else:
            content = text_interaction

        self.update_conversation_history(role="user", content=content)

        response = self.groq_client.chat.completions.create(
            messages=self.conversation_history,
            model="qwen/qwen3.8-27b",
            include_reasoning=False,
        ).choices[0].message.content

        self.update_conversation_history(role="assistant", content=response)

        return response


if __name__ == "__main__":
    agent = ConversationAgent()
    question = input("Pose ta question :\n")
    response = agent.ask_llm(question)
    print("\n")
    print(response)
