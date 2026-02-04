"""
PolyGlot - Advanced Language Translation with Text-to-Speech
Run: streamlit run polyglot.py
"""

import streamlit as st
from gtts import gTTS
from deep_translator import GoogleTranslator
from io import BytesIO
from datetime import datetime

# ---------------- LANGUAGES ---------------- #
LANGUAGES = {
    'af': 'Afrikaans', 'ar': 'Arabic', 'bn': 'Bengali', 'zh-CN': 'Chinese (Simplified)',
    'zh-TW': 'Chinese (Traditional)', 'cs': 'Czech', 'da': 'Danish', 'nl': 'Dutch',
    'en': 'English', 'fi': 'Finnish', 'fr': 'French', 'de': 'German', 'el': 'Greek',
    'hi': 'Hindi', 'hu': 'Hungarian', 'id': 'Indonesian', 'it': 'Italian', 'ja': 'Japanese',
    'ko': 'Korean', 'ms': 'Malay', 'ne': 'Nepali', 'no': 'Norwegian', 'pl': 'Polish',
    'pt': 'Portuguese', 'pa': 'Punjabi', 'ru': 'Russian', 'es': 'Spanish', 'sv': 'Swedish',
    'ta': 'Tamil', 'te': 'Telugu', 'th': 'Thai', 'tr': 'Turkish', 'uk': 'Ukrainian',
    'ur': 'Urdu', 'vi': 'Vietnamese'
}

# ---------------- FUNCTIONS ---------------- #
def translate_text(text, source_lang, target_lang):
    try:
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        return translator.translate(text), None
    except Exception as e:
        return None, str(e)

def text_to_speech(text, lang):
    try:
        tts = gTTS(text=text, lang=lang.lower())
        audio = BytesIO()
        tts.write_to_fp(audio)
        audio.seek(0)
        return audio, None
    except Exception as e:
        return None, str(e)

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(page_title="PolyGlot Translator", layout="wide", page_icon="🌐")

# ---------------- BACKGROUND & UI STYLE ---------------- #
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #667eea, #764ba2);
}

.main {
    background-color: rgba(255,255,255,0.08);
    backdrop-filter: blur(10px);
}

h1, h2, h3 {
    color: white;
    text-align: center;
}

textarea {
    border-radius: 12px !important;
}

button {
    border-radius: 12px !important;
    font-weight: bold !important;
}

.block-container {
    padding-top: 2rem;
}

.card {
    background: rgba(255,255,255,0.15);
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.2);
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ---------------- #
if "trans_result" not in st.session_state:
    st.session_state.trans_result = ""
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- HEADER ---------------- #
st.markdown("<h1>🌐 PolyGlot Translator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#ddd;'>Translate and listen in many languages</p>", unsafe_allow_html=True)
st.divider()

col1, col2 = st.columns(2)

# ---------- SOURCE ----------
with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 📝 Input")

    source_lang = st.selectbox(
        "Choose Input language",
        ["auto"] + list(LANGUAGES.keys()),
        format_func=lambda x: "Auto Detect" if x == "auto" else LANGUAGES[x]
    )

    source_text = st.text_area(
        "",
        placeholder="Type or paste text here...",
        height=220
    )

    if st.button("🔊 Listen", use_container_width=True):
        if source_lang == "auto":
            st.warning("Select a language for speech.")
        else:
            audio, err = text_to_speech(source_text, source_lang)
            if audio:
                st.audio(audio)
            else:
                st.error(err)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------- TARGET ----------
with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 🌍 Translation")

    target_lang = st.selectbox(
        "Choose Translation language",
        list(LANGUAGES.keys()),
        format_func=lambda x: LANGUAGES[x]
    )

    st.text_area(
        "",
        value=st.session_state.trans_result,
        placeholder="Translation will appear here...",
        height=220,
        disabled=True
    )

    if st.button("🔊 Listen to Translation", use_container_width=True):
        if st.session_state.trans_result:
            audio, err = text_to_speech(st.session_state.trans_result, target_lang)
            if audio:
                st.audio(audio)
            else:
                st.error(err)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------- TRANSLATE ----------
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🚀 Translate", type="primary", use_container_width=True):
    if not source_text.strip():
        st.warning("Please enter text")
    else:
        translated, error = translate_text(source_text, source_lang, target_lang)
        if translated:
            st.session_state.trans_result = translated
            st.session_state.history.append({
                "time": datetime.now().strftime("%H:%M:%S"),
                "source_lang": "Auto" if source_lang=="auto" else LANGUAGES[source_lang],
                "target_lang": LANGUAGES[target_lang],
                "source": source_text,
                "translated": translated
            })
            st.success("✅ Translation completed")
            st.rerun()
        else:
            st.error(error)

# ---------- HISTORY ----------
if st.session_state.history:
    with st.expander("🕘 Recent Translations"):
        for item in reversed(st.session_state.history[-5:]):
            st.markdown(f"**{item['source_lang']} → {item['target_lang']}**")
            st.markdown(f"Input: {item['source']}")
            st.markdown(f"Output: {item['translated']}")
            st.markdown("---")