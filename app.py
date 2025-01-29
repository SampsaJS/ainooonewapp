import streamlit as st

st.markdown("🚀 Sovellus latautuu onnistuneesti...")

from assistant import get_chat_response
from dotenv import load_dotenv
import os

# Ladataan ympäristömuuttujat
load_dotenv()

# Haetaan API-avain
openai_api_key = os.getenv("OPENAI_API_KEY")

# Tarkistetaan API-avain
if not openai_api_key:
    st.error("OpenAI API -avain puuttuu .env-tiedostosta!")
    st.stop()

# Sovelluksen ulkoasu
st.title("💬 SNAPIN AiNooo")
st.caption("Valitse malli ja aloita keskustelu")

# Mallin valinta
model_choice = st.selectbox(
    "Valitse malli:",
    ["gpt-3.5-turbo", "gpt-4"],
    key="model_selector"
)

# Alustetaan viestihistoria
if "messages" not in st.session_state:
    st.session_state.messages = []

# Näytetään kaikki vanhat viestit
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Keskustelun käsittely
if prompt := st.chat_input("Kirjoita viesti..."):
    # Lisätään käyttäjän viesti historiaan
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Näytetään käyttäjän viesti
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generoidaan vastaus
    try:
        with st.spinner("Ajatellaan..."):
            full_response = get_chat_response(
                model=model_choice,
                user_input=prompt,
                messages=st.session_state.messages,
                api_key=openai_api_key
            )
        
        # Lisätään ja näytetään vastaus
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        with st.chat_message("assistant"):
            st.markdown(full_response)

    except Exception as e:
        st.error(f"Virhe keskustelun käsittelyssä: {str(e)}")
