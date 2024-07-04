import openai
import logging

class OpenAIProcessor:
    def __init__(self, parent):
        self.parent = parent
        openai.api_key = "your_openai_api_key"  # Replace with your actual OpenAI API key
        logging.info("OpenAIProcessor initialized")

    def process_text(self, text):
        try:
            response = openai.Completion.create(
                engine="davinci",
                prompt=text,
                max_tokens=150
            )
            return response.choices[0].text.strip()
        except Exception as e:
            error_message = f"Error during text processing: {str(e)}"
            logging.error(error_message)
            self.parent.error_signal.emit(error_message)
            return ""
