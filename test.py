import os
from dotenv import load_dotenv
import openai

# Load environment variables from the .env file
load_dotenv()

# Set the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OpenAI API key not found. Please ensure it's set in the .env file.")

# Example API call
try:
    response = openai.ChatCompletion.create(
        model="gpt-4",  # or "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Write a haiku about AI."}
        ],
        max_tokens=50
    )
    print("Response from GPT:")
    print(response["choices"][0]["message"]["content"].strip())
except openai.error.AuthenticationError:
    print("Invalid API key. Please check your API key and try again.")
except openai.error.RateLimitError:
    print("Rate limit exceeded. Check your usage and billing details.")
except Exception as e:
    print(f"An error occurred: {e}")
