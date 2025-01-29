import openai
from typing import Optional

def get_chat_response(model: str, user_input: str, messages: list, api_key: str) -> Optional[str]:
    openai.api_key = api_key
    
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages + [{"role": "user", "content": user_input}],
            temperature=0.7,
            max_tokens=1500,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        return response.choices[0].message['content'].strip()
    
    except openai.error.AuthenticationError:
        return "Virhe: Väärä API-avain"
    except openai.error.RateLimitError:
        return "Virhe: API-kutsu rajoitus ylitetty"
    except Exception as e:
        return f"Virhe: {str(e)}"