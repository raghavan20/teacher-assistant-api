import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

class Chatbot:
    def __init__(self, api_key, model_name="gemini-pro"):
        """Initialize the Chatbot with a Google API Key and LLM model."""
        self.api_key = api_key
        self.model_name = model_name
        self.conversation = self.init_gemini_llm()

    def init_gemini_llm(self):
        """Initialize the Gemini large language model (LLM)."""
        try:
            llm = ChatGoogleGenerativeAI(model=self.model_name, google_api_key=self.api_key)
            memory = ConversationBufferMemory()
            conversation = ConversationChain(
                llm=llm,
                memory=memory,
                verbose=False
            )
            return conversation
        except Exception as e:
            print(f"Error initializing LLM: {e}")
            return None

    def get_response(self, user_input):
        """Send a prompt to the chatbot and receive a formatted response."""
        if self.conversation:
            try:
                response = self.conversation.predict(input=user_input)
                return self.format_response(response)
            except Exception as e:
                print(f"Error during conversation: {e}")
                return None
        else:
            print("Conversation chain not initialized.")
            return None

    def format_response(self, text, max_line_length=10):
        """Format the response to ensure line length does not exceed max_line_length."""
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            if len(current_line) + len(word) + 1 > max_line_length:
                lines.append(current_line)
                current_line = word
            else:
                if current_line:
                    current_line += " "
                current_line += word

        if current_line:  # Add any remaining words as the last line
            lines.append(current_line)

        return '\n'.join(lines)


def main():
    """Main function to run the chatbot application."""
    # It is recommended to pass the API key securely via environment variable
    # api_key = os.environ.get("GOOGLE_API_KEY")
    api_key = 'AIzaSyATpYDgbBeJJD-0V7OQw-V7yEzy0VUtZ8c'

    bot = Chatbot(api_key=api_key)

    if bot.conversation:
        print("Welcome to the Gemini Chatbot! Type 'exit' to quit.")

        while True:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                break

            response = bot.get_response(user_input)
            if response:
                print("Bot:", response)
            else:
                print("Failed to get a response. Check for errors above.")
    else:
        print("Failed to initialize the chatbot. Check for errors above.")


if __name__ == "__main__":
    main()
