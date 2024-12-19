import os
import re
import openai
import dotenv
from config import PROMPT_TEMPLATE

dotenv.load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# used LLM to do more efficiently
def clean(text: str) -> int:
    temp = str(text).strip()
    cleaned = re.sub(r'[^\d.]', '', temp)
    try:
        return int(float(cleaned))
    except ValueError:
        return None

def get_response(test_case: dict, model_name: str):
    prompt = PROMPT_TEMPLATE.format(**test_case)

    response = client.chat.completions.create(model=model_name,
    messages=[
        {"role": "system", "content": "You are a rental price recommendation system."},
        {"role": "user", "content": prompt}
    ], temperature=0.7, max_tokens=10)

    price_text = response.choices[0].message.content.strip()
    rental_price = clean(price_text)
    return {**test_case, "Rental Price": rental_price}
