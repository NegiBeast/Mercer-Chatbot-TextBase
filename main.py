import textbase
from textbase.message import Message
from textbase import models
import os
from typing import List

# Load your OpenAI API key
models.OpenAI.api_key = "YOUR_API_KEY"
# or from environment variable:
# models.OpenAI.api_key = os.getenv("OPENAI_API_KEY")

# Prompt for starting the conversation
WELCOME_PROMPT = """Welcome to the ChatBot! Feel free to ask anything or talk about any topic. The AI will respond naturally. Let's start the conversation!
"""

@textbase.chatbot("talking-bot")
def on_message(message_history: List[Message], state: dict = None):
    """Your chatbot logic here
    message_history: List of user messages
    state: A dictionary to store any stateful information

    Return a string with the bot_response or a tuple of (bot_response: str, new_state: dict)
    """
    if state is None:
        state = {"counter": 0}
    else:
        state["counter"] = state.get("counter", 0) + 1

    # Combine all user messages for context
    user_messages = "\n".join(message.text for message in message_history)

    # Generate GPT-3.5 Turbo response
    bot_response = models.OpenAI.generate(
        system_prompt=WELCOME_PROMPT + user_messages,
        model="gpt-3.5-turbo",
    )

    return bot_response, state

# Main loop for user interactions
def main():
    print("ChatBot: Initializing...")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("ChatBot: Goodbye!")
            break

        # Create a user message
        user_message = Message(user_input, role=Message.Role.USER)

        # Call the chatbot function to get a response
        bot_response, _ = on_message([user_message])

        print(f"ChatBot: {bot_response}")

if __name__ == "__main__":
    main()
