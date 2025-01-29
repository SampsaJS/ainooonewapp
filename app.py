import streamlit as st
from assistant import get_chat_response
from dotenv import load_dotenv
import os

# Ladataan ympäristömuuttujat
load_dotenv()

# Asetetaan sivun konfiguraatio
st.set_page_config(
    page_title="SNAPIN AiNooo",
    page_icon="🤖",
    layout="centered"
)

# Haetaan API-avain ja tarkistetaan se
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    st.error("🔑 OpenAI API -avain puuttuu! Lisää se .env-tiedostoon tai Streamlitin asetuksiin.")
    st.stop()

# Alustetaan viestihistoria
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Olet suomenkielinen tekoälyavustaja."}
    ]

# Näyttää otsikon
st.title("💬 SNAPIN AiNooo")
st.caption("Suomenkielinen tekoälyavustaja")

# Mallin valinta
model_choice = st.sidebar.selectbox(
    "Valitse malli:",
    ["gpt-3.5-turbo", "gpt-4"],
    key="model_selector"
)

# Näyttää viestihistorian
for message in st.session_state.messages:
    if message["role"] != "system":  # Ei näytetä järjestelmäviestejä
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Käsittelee käyttäjän syötteen
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
                messages=st.session_state.messages,
                api_key=openai_api_key
            )
        
        # Lisätään vastaus historiaan
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
        # Näytetään vastaus
        with st.chat_message("assistant"):
            st.markdown(full_response)

    except Exception as e:
        st.error(f"Virhe: {str(e)}")
