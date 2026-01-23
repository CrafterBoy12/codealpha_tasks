import streamlit as st
from gtts import gTTS
from deep_translator import GoogleTranslator
from io import BytesIO
import time

# ---------------------
# Language Data
# ---------------------
LANGUAGES = {
    'af': 'Afrikaans', 'sq': 'Albanian', 'am': 'Amharic', 'ar': 'Arabic',
    'hy': 'Armenian', 'az': 'Azerbaijani', 'eu': 'Basque', 'be': 'Belarusian',
    'bn': 'Bengali', 'bs': 'Bosnian', 'bg': 'Bulgarian', 'ca': 'Catalan',
    'ceb': 'Cebuano', 'zh-CN': 'Chinese (Simplified)', 'zh-TW': 'Chinese (Traditional)',
    'co': 'Corsican', 'hr': 'Croatian', 'cs': 'Czech', 'da': 'Danish',
    'nl': 'Dutch', 'en': 'English', 'eo': 'Esperanto', 'et': 'Estonian',
    'fi': 'Finnish', 'fr': 'French', 'fy': 'Frisian', 'gl': 'Galician',
    'ka': 'Georgian', 'de': 'German', 'el': 'Greek', 'gu': 'Gujarati',
    'ht': 'Haitian Creole', 'ha': 'Hausa', 'haw': 'Hawaiian', 'he': 'Hebrew',
    'hi': 'Hindi', 'hmn': 'Hmong', 'hu': 'Hungarian', 'is': 'Icelandic',
    'ig': 'Igbo', 'id': 'Indonesian', 'ga': 'Irish', 'it': 'Italian',
    'ja': 'Japanese', 'jw': 'Javanese', 'kn': 'Kannada', 'kk': 'Kazakh',
    'km': 'Khmer', 'rw': 'Kinyarwanda', 'ko': 'Korean', 'ku': 'Kurdish',
    'ky': 'Kyrgyz', 'lo': 'Lao', 'la': 'Latin', 'lv': 'Latvian',
    'lt': 'Lithuanian', 'lb': 'Luxembourgish', 'mk': 'Macedonian', 'mg': 'Malagasy',
    'ms': 'Malay', 'ml': 'Malayalam', 'mt': 'Maltese', 'mi': 'Maori',
    'mr': 'Marathi', 'mn': 'Mongolian', 'my': 'Myanmar (Burmese)', 'ne': 'Nepali',
    'no': 'Norwegian', 'ny': 'Nyanja (Chichewa)', 'or': 'Odia (Oriya)', 'ps': 'Pashto',
    'fa': 'Persian', 'pl': 'Polish', 'pt': 'Portuguese', 'pa': 'Punjabi',
    'ro': 'Romanian', 'ru': 'Russian', 'sm': 'Samoan', 'gd': 'Scots Gaelic',
    'sr': 'Serbian', 'st': 'Sesotho', 'sn': 'Shona', 'sd': 'Sindhi',
    'si': 'Sinhala', 'sk': 'Slovak', 'sl': 'Slovenian', 'so': 'Somali',
    'es': 'Spanish', 'su': 'Sundanese', 'sw': 'Swahili', 'sv': 'Swedish',
    'tl': 'Tagalog (Filipino)', 'tg': 'Tajik', 'ta': 'Tamil', 'tt': 'Tatar',
    'te': 'Telugu', 'th': 'Thai', 'tr': 'Turkish', 'tk': 'Turkmen',
    'uk': 'Ukrainian', 'ur': 'Urdu', 'ug': 'Uyghur', 'uz': 'Uzbek',
    'vi': 'Vietnamese', 'cy': 'Welsh', 'xh': 'Xhosa', 'yi': 'Yiddish',
    'yo': 'Yoruba', 'zu': 'Zulu'
}

TTS_SUPPORTED_LANGS = [
    'af', 'ar', 'bg', 'bn', 'bs', 'ca', 'cs', 'da', 'de', 'el', 'en', 'es', 
    'et', 'fi', 'fr', 'gu', 'hi', 'hr', 'hu', 'id', 'is', 'it', 'iw', 'ja', 
    'jw', 'km', 'kn', 'ko', 'la', 'lv', 'ml', 'mr', 'ms', 'my', 'ne', 'nl', 
    'no', 'pl', 'pt', 'ro', 'ru', 'si', 'sk', 'sq', 'sr', 'su', 'sv', 'sw', 
    'ta', 'te', 'th', 'tl', 'tr', 'uk', 'ur', 'vi', 'zh-CN', 'zh-TW'
]

def is_tts_supported(lang_code):
    return lang_code in TTS_SUPPORTED_LANGS

def translate_text(text, source_lang, target_lang):
    try:
        translator = GoogleTranslator(source='auto' if source_lang=='auto' else source_lang, target=target_lang)
        return translator.translate(text), None
    except Exception as e:
        return None, str(e)

def text_to_speech(text, lang):
    try:
        tts_lang = {'zh-CN':'zh-cn','zh-TW':'zh-tw','he':'iw'}.get(lang, lang)
        if not is_tts_supported(tts_lang):
            return None
        tts = gTTS(text=text, lang=tts_lang, slow=False)
        audio_bytes = BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        return audio_bytes.read()
    except:
        return None

# ---------------------
# Page Config
# ---------------------
st.set_page_config(
    page_title="PolyGlot Pro",
    page_icon="🈷️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern look
st.markdown("""
<style>
/* Gradient header */
.main-header {
    text-align: center;
    font-size: 3rem;
    font-weight: bold;
    background: linear-gradient(to right, #6366f1, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 20px 0;
}

/* Translation box */
.translation-box {
    padding: 20px;
    border-radius: 12px;
    min-height: 250px;
    font-size: 16px;
    line-height: 1.6;
    box-shadow: 0 0 15px rgba(0,0,0,0.5);
}

/* Buttons */
.stButton > button {
    background-color: #6366f1;
    color: white;
    font-weight: bold;
    border-radius: 8px;
    padding: 8px 20px;
}
.stButton > button:hover {
    background-color: #4f46e5;
}
</style>
""", unsafe_allow_html=True)

# ---------------------
# Header
# ---------------------
st.markdown("<h1 class='main-header'>PolyGlot Pro</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9ca3af;'>Translate across 110+ languages with Text-to-Speech 🎤</p>", unsafe_allow_html=True)
st.markdown("---")

# ---------------------
# Language Selection
# ---------------------
col1, col2, col3 = st.columns([5,1,5])

with col1:
    st.subheader("Source Language")
    source_lang = st.selectbox("From", options=['auto'] + list(LANGUAGES.keys()),
                               format_func=lambda x: "Auto Detect" if x=='auto' else LANGUAGES[x])

with col2:
    if st.button("🔄 Swap Languages"):
        st.info("Swap feature placeholder")

with col3:
    st.subheader("Target Language")
    target_lang = st.selectbox("To", options=list(LANGUAGES.keys()), 
                               index=list(LANGUAGES.keys()).index('ur'),
                               format_func=lambda x: LANGUAGES[x])

st.markdown("---")

# ---------------------
# Text Areas
# ---------------------
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Enter Text")
    source_text = st.text_area("", placeholder="Type your text here...", height=250)

with col2:
    st.markdown("### Translation")
    translation_container = st.container()
    if 'trans_result' not in st.session_state:
        st.session_state.trans_result = ""
    if st.session_state.trans_result:
        st.markdown(f"<div class='translation-box' style='background-color:#1e293b;color:white;border:1px solid #444'>{st.session_state.trans_result}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='translation-box' style='background-color:#1e293b;color:#888;border:1px dashed #444;display:flex;justify-content:center;align-items:center;font-style:italic;'>Translation will appear here...</div>", unsafe_allow_html=True)

# ---------------------
# Translate Button
# ---------------------
col1, col2, col3 = st.columns([3,4,3])
with col2:
    if st.button("🚀 Translate Now"):
        if source_text.strip():
            progress = st.progress(0)
            status = st.empty()
            status.text("Translating...")
            progress.progress(40)
            translated, error = translate_text(source_text, source_lang, target_lang)
            progress.progress(80)
            if translated:
                st.session_state.trans_result = translated
                progress.progress(100)
                status.text("✅ Translation Complete")
                st.success("Translation successful!")
                st.rerun()
            else:
                status.text("")
                st.error(f"Error: {error}")
        else:
            st.warning("Enter text to translate")

# ---------------------
# Footer
# ---------------------
st.markdown("---")
st.markdown("<p style='text-align:center;color:#9ca3af;'>Powered by Google Translate & Google TTS | Supports 110+ languages</p>", unsafe_allow_html=True)
