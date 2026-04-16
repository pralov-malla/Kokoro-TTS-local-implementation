from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))


SYSTEM_PROMPT = (
    "You are a US visa interview officer conducting an F1 student visa interview.\n"
    "Use a two sentence and keep it under 50 words when possible.\n"
    "Use clear punctuation for natural speech. Be formal but approachable.\n"
    "Remember previous answers. RESPOND ONLY WITH YOUR QUESTION."
)

class ConversationManager:
    def __init__(self):
        self.messages = []

    
    def stream_response(self, user_input):

        user_input = user_input.strip()

        if not user_input:
            return 
        

        self.messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model = "gpt-4.1-mini",
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                *self.messages],
            stream = True,
            temperature = 0.7,
            max_tokens = 100,
        )

        for chunk in response:
            if chunk.choices:
                delta = chunk.choices[0].delta
                text = getattr(delta, "content", "") or ""
                if text:
                    yield text
    
    def add_assistant_message(self, text):
        self.messages.append({"role": "assistant", "content": text})

    def reset(self):
        self.messages = []
                
        
