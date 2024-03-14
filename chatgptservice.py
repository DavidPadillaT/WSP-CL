from openai import OpenAI
import logging
from dotenv import load_dotenv
import os

logging.basicConfig(level=logging.INFO)

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def get_response():
    try:
        response  = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
                {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
            ]
        )
        return response.choices[0].message
    except Exception as e:
        logging.error(f"Error: {e}")
        return "error"
    
get_response()

if __name__ == "__main__":
    get_response()