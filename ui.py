import streamlit as st
import speech_recognition as sr
from googletrans import Translator
from streamlit_autorefresh import st_autorefresh


recognizer = sr.Recognizer()
translator = Translator()
CHUNK_DURATION = 20  

# Initialize session state
if "is_listening" not in st.session_state:
    st.session_state.is_listening = False

st.title("Real-Time Arabic Speech ➜ German Translator 🎙️")

# Control buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("Start Listening"):
        st.session_state.is_listening = True
with col2:
    if st.button("⏹ Stop Listening"):
        st.session_state.is_listening = False

# Auto-refresh every 21 seconds only if listening
if st.session_state.is_listening:
    st_autorefresh(interval=21000, limit=None, key="loop_refresh")
    st.success("✅ Listening... (Recording for 20 seconds)")

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.record(source, duration=CHUNK_DURATION)

    try:
        # Speech to Text (Arabic)
        arabic_text = recognizer.recognize_google(audio, language='ar')
        st.markdown(f"**🗣️ Arabic:** {arabic_text}")

        # Translation to German
        translated = translator.translate(arabic_text, src='ar', dest='de')
        st.markdown(f"**🇩🇪 German:** {translated.text}")

    except sr.UnknownValueError:
        st.error("❌ Could not understand the audio.")
    except sr.RequestError as e:
        st.error(f"⚠️ API error: {e}")

