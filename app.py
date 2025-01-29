import streamlit as st
from assistant import get_chat_response

# Sivun perusasetukset
st.set_page_config(
    page_title="SNAPIN AiNooo",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Tyylitiedot
st.markdown("""
<style>
    [data-testid=stSidebar] {
        background: #f0f2f6 !important;
    }
    .stChatInput input {
        border: 2px solid #4a90e2 !important;
    }
</style>
""", unsafe_allow_html=True)

# API-avaimen haku
try:
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
except (KeyError, AttributeError) as e:
    st.error("🔑 API-avain puuttuu! Lisää se Streamlitin Secrets-osiossa.")
    st.stop()

# Alustetaan viestihistoria
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Miten voin auttaa sinua tänään?"}
    ]

# Sivupalkin sisältö
with st.sidebar:
    st.header("⚙️ Asetukset")
    model_name = st.selectbox(
        "Valitse malli:",
        ["gpt-3.5-turbo", "gpt-4"],
        index=0,
        key="model_selector"
    )
    st.divider()
    st.markdown("**Tietoturva:**")
    st.markdown("- Kaikki viestit salataan")
    st.markdown("- Tietoja ei tallenneta")

# Pääsisältö
st.title("💬 SNAPIN AiNooo")
st.caption("Suomenkielinen tekoälyavustaja GPT-teknologialla")

# Näytä viestihistoria
for message in st.session_state.messages:
    avatar = "🤖" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Käsittele uusi viesti
if prompt := st.chat_input("Kirjoita viestisi tähän..."):
    # Lisää käyttäjän viesti historiaan
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Näytä käyttäjän viesti
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Generoi vastaus
    try:
        with st.spinner("Generoidaan vastausta..."):
            response = get_chat_response(
                model=model_name,
                messages=st.session_state.messages,
                api_key=OPENAI_API_KEY
            )
        
        # Lisää vastaus historiaan
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Näytä vastaus
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(response)

    except Exception as e:
        st.error(f"Virhe: {str(e)}")
