import openai
from typing import Union

def get_chat_response(model: str, messages: list, api_key: str) -> Union[str, None]:
    try:
        openai.api_key = api_key
        
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
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
        return "Virhe: Kutsuraja ylitetty - yritä hetken kuluttua"
    except openai.error.APIError as e:
        return f"API-virhe: {str(e)}"
    except Exception as e:
        return f"Odottamaton virhe: {str(e)}"
