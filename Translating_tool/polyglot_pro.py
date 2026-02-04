"""
PolyGlot - Advanced Language Translation with Text-to-Speech
Run: streamlit run polyglot.py
"""

import streamlit as st
from gtts import gTTS
from deep_translator import GoogleTranslator
from io import BytesIO
from datetime import datetime

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="PolyGlot Translator",
    layout="wide",
    page_icon="🌐"
)

# ---------------- CUSTOM CSS ---------------- #
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}

.main {
    background-color: transparent;
}

h1, h2, h3 {
    color: #ffffff;
}

p {
    color: #cccccc;
}

.card {
    background: rgba(255,255,255,0.05);
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0px 0px 15px rgba(0,0,0,0.4);
}

textarea {
    background-color: #1e1e1e !important;
    color: white !important;
    border-radius: 10px !important;
}

select {
    background-color: #1e1e1e !important;
    color: white !important;
}

button {
    border-radius: 12px !important;
    font-weight: bold !important;
}

hr {
    border-color: #444;
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LANGUAGES ---------------- #
LANGUAGES = {
    'af': 'Afrikaans', 'sq': 'Albanian', 'am': 'Amharic', 'ar': 'Arabic',
    'hy': 'Armenian', 'az': 'Azerbaijani', 'eu': 'Basque', 'be': 'Belarusian',
    'bn': 'Bengali', 'bs': 'Bosnian', 'bg': 'Bulgarian', 'ca': 'Catalan',
    'ceb': 'Cebuano', 'ny': 'Chichewa', 'zh-CN': 'Chinese (Simplified)',
    'zh-TW': 'Chinese (Traditional)', 'co': 'Corsican', 'hr': 'Croatian',
    'cs': 'Czech', 'da': 'Danish', 'nl': 'Dutch', 'en': 'English',
    'eo': 'Esperanto', 'et': 'Estonian', 'tl': 'Filipino', 'fi': 'Finnish',
    'fr': 'French', 'fy': 'Frisian', 'gl': 'Galician', 'ka': 'Georgian',
    'de': 'German', 'el': 'Greek', 'gu': 'Gujarati', 'ht': 'Haitian Creole',
    'ha': 'Hausa', 'haw': 'Hawaiian', 'iw': 'Hebrew', 'hi': 'Hindi',
    'hmn': 'Hmong', 'hu': 'Hungarian', 'is': 'Icelandic', 'ig': 'Igbo',
    'id': 'Indonesian', 'ga': 'Irish', 'it': 'Italian', 'ja': 'Japanese',
    'jw': 'Javanese', 'kn': 'Kannada', 'kk': 'Kazakh', 'km': 'Khmer',
    'rw': 'Kinyarwanda', 'ko': 'Korean', 'ku': 'Kurdish (Kurmanji)',
    'ky': 'Kyrgyz', 'lo': 'Lao', 'la': 'Latin', 'lv': 'Latvian',
    'lt': 'Lithuanian', 'lb': 'Luxembourgish', 'mk': 'Macedonian',
    'mg': 'Malagasy', 'ms': 'Malay', 'ml': 'Malayalam', 'mt': 'Maltese',
    'mi': 'Maori', 'mr': 'Marathi', 'mn': 'Mongolian', 'my': 'Myanmar (Burmese)',
    'ne': 'Nepali', 'no': 'Norwegian', 'or': 'Odia', 'ps': 'Pashto',
    'fa': 'Persian', 'pl': 'Polish', 'pt': 'Portuguese', 'pa': 'Punjabi',
    'ro': 'Romanian', 'ru': 'Russian', 'sm': 'Samoan', 'gd': 'Scots Gaelic',
    'sr': 'Serbian', 'st': 'Sesotho', 'sn': 'Shona', 'sd': 'Sindhi',
    'si': 'Sinhala', 'sk': 'Slovak', 'sl': 'Slovenian', 'so': 'Somali',
    'es': 'Spanish', 'su': 'Sundanese', 'sw': 'Swahili', 'sv': 'Swedish',
    'tg': 'Tajik', 'ta': 'Tamil', 'te': 'Telugu', 'th': 'Thai',
    'tr': 'Turkish', 'uk': 'Ukrainian', 'ur': 'Urdu', 'uz': 'Uzbek',
    'vi': 'Vietnamese', 'cy': 'Welsh', 'xh': 'Xhosa', 'yi': 'Yiddish',
    'yo': 'Yoruba', 'zu': 'Zulu'
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

# ---------------- SESSION STATE ---------------- #
if "trans_result" not in st.session_state:
    st.session_state.trans_result = ""
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- HEADER ---------------- #
st.markdown("""
<h1 style='text-align:center;'>🌐 PolyGlot Translator</h1>
<p style='text-align:center;'>Translate and listen in multiple languages</p>
<hr>
""", unsafe_allow_html=True)

# ---------------- MAIN LAYOUT ---------------- #
col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 📝 Input")

    source_lang = st.selectbox(
        "Choose Input language",
        ["auto"] + list(LANGUAGES.keys()),
        format_func=lambda x: "Auto Detect" if x == "auto" else LANGUAGES[x]
    )

    source_text = st.text_area(
        "Enter Text",
        placeholder="Type or paste text here...",
        height=200
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

with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 🌍 Translation")

    target_lang = st.selectbox(
        "Choose Translation language",
        list(LANGUAGES.keys()),
        format_func=lambda x: LANGUAGES[x]
    )

    st.text_area(
        "Translated Text",
        value=st.session_state.trans_result,
        placeholder="Translation will appear here...",
        height=200,
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

# ---------------- TRANSLATE BUTTON ---------------- #
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
            st.success("Translation completed")
            st.rerun()
        else:
            st.error(error)

# ---------------- HISTORY ---------------- #
if st.session_state.history:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    with st.expander("🕘 Recent Translations"):
        for item in reversed(st.session_state.history[-5:]):
            st.markdown(f"**{item['source_lang']} → {item['target_lang']}**")
            st.markdown(f"Input: {item['source']}")
            st.markdown(f"Output: {item['translated']}")
            st.markdown("---")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- FOOTER ---------------- #
st.markdown("""
<hr>
<p style='text-align:center;color:#aaa;'>PolyGlot Translator © 2026 | Professional UI Edition</p>
""", unsafe_allow_html=True)