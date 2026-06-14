import streamlit as st
from modules.pdf_extractor import extract_text_from_pdf
from modules.summarizer import generate_summary
from modules.quiz_generator import generate_quiz
from utils.helpers import chunk_text
import random
import base64

st.set_page_config(page_title="AI Study Assistant - ZUST", page_icon="🌿", layout="wide")

def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

logo_base64 = get_image_base64("logo.png")

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Tajawal:wght@400;700;900&display=swap');

    * {{ font-family: 'Tajawal', sans-serif; }}

    .stApp {{
        background: linear-gradient(160deg, #060f06 0%, #0f1f0f 40%, #060f06 100%);
    }}

    .main-header {{
        text-align: center;
        padding: 2.5rem 1rem;
        background: linear-gradient(135deg, #0d1f0d, #1a3a1a);
        border-radius: 24px;
        border: 2px solid #c9a227;
        margin-bottom: 2rem;
        box-shadow: 0 0 40px rgba(201,162,39,0.25), inset 0 0 60px rgba(0,0,0,0.3);
    }}

    .main-header img {{
        width: 110px;
        margin-bottom: 1rem;
        filter: drop-shadow(0 0 12px rgba(201,162,39,0.5));
    }}

    .main-header h1 {{
        font-family: 'Playfair Display', serif;
        color: #c9a227;
        font-size: 2.8rem;
        font-weight: 900;
        margin: 0;
        letter-spacing: 2px;
        text-shadow: 0 0 25px rgba(201,162,39,0.6);
    }}

    .main-header .subtitle {{
        color: #90c878;
        font-size: 1.05rem;
        margin-top: 0.5rem;
        letter-spacing: 1px;
    }}

    .welcome-banner {{
        background: linear-gradient(135deg, #1a3314, #2a4a1a);
        border: 1px solid #c9a227;
        border-radius: 16px;
        padding: 1rem 2rem;
        text-align: center;
        color: #f5e6b0;
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(201,162,39,0.15);
        letter-spacing: 1px;
    }}

    .funny-box {{
        background: linear-gradient(135deg, #1a2e10, #243d18);
        border: 1px solid #c9a227;
        border-radius: 14px;
        padding: 0.9rem 1.5rem;
        margin: 1rem 0;
        color: #f5e6b0;
        font-size: 1.05rem;
        text-align: center;
        font-weight: 700;
    }}

    .result-box {{
        background: linear-gradient(135deg, #0a1f0a, #102010);
        border: 1px solid #4a8a3a;
        border-radius: 16px;
        padding: 2rem;
        color: #dff0d8;
        line-height: 2;
        font-size: 1.05rem;
        box-shadow: inset 0 0 30px rgba(0,0,0,0.3);
    }}

    .stButton > button {{
        background: linear-gradient(135deg, #c9a227, #a07d1a) !important;
        color: #0a1a0a !important;
        font-family: 'Playfair Display', serif !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        width: 100% !important;
        letter-spacing: 1px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(201,162,39,0.3) !important;
    }}

    .stButton > button:hover {{
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(201,162,39,0.5) !important;
    }}

    .stTabs [data-baseweb="tab-list"] {{
        background: transparent !important;
        border-bottom: 2px solid #2a4a1a !important;
    }}

    .stTabs [data-baseweb="tab"] {{
        color: #90c878 !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        letter-spacing: 1px !important;
    }}

    .stTabs [aria-selected="true"] {{
        color: #c9a227 !important;
        border-bottom: 3px solid #c9a227 !important;
    }}

    .stFileUploader {{
        background: linear-gradient(135deg, #0f2010, #1a3a1a) !important;
        border: 2px dashed #4a8a3a !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
    }}

    .footer {{
        text-align: center;
        color: #4a7a3a;
        padding: 1.5rem;
        margin-top: 2rem;
        border-top: 1px solid #2a4a1a;
        font-size: 0.9rem;
        letter-spacing: 1px;
    }}

    div[data-testid="stMarkdownContainer"] p {{ color: #dff0d8; }}
</style>
""", unsafe_allow_html=True)

funny_loading = [
    "🧠 الذكاء الاصطناعي بيقرأ أسرع منك...",
    "☕ اتفضل اشرب قهوة، لازم دقيقة...",
    "🤖 الروبوت بيذاكر عنك هلق...",
    "📚 لو ذاكرت بنفسك كان أسرع 😂",
    "⚡ بيشتغل بسرعة الضوء... تقريباً!",
]

funny_summary_done = [
    "✅ ع قولة الدكتور بلال: شوووي شووووي... خلص الملخص! 😄",
    "🎉 ع قولة الدكتور بلال: بتعوضو بالفاينل — بس هلق ذاكر! 😂",
    "🏆 يلي بعرف الاشتقاق الدكتور بلال بحطله 99 — هلق اشتق! 😂",
]

funny_quiz_done = "🎯 بكفيكم خمسة أسئلة... مثل عدد أسئلة الدكتور بلال بالامتحان! 😂"

# Header
st.markdown(f"""
<div class="main-header">
    <img src="data:image/png;base64,{logo_base64}" alt="ZUST Logo"/>
    <h1>AI Study Assistant</h1>
    <div class="subtitle">جامعة الزيتونة للعلوم والتكنولوجيا</div>
</div>
""", unsafe_allow_html=True)

# Welcome Banner
st.markdown("""
<div class="welcome-banner">
    🌿 ع قولة الدكتور بلال: يا هلااااااااا! أهلاً بك بمساعدك الذكي للدراسة 🌿
</div>
""", unsafe_allow_html=True)

# Upload
uploaded_file = st.file_uploader("📄 ارفع ملف PDF هون", type=["pdf"])

if uploaded_file:
    with st.spinner(random.choice(funny_loading)):
        text = extract_text_from_pdf(uploaded_file)
        text = chunk_text(text)

    st.markdown('<div class="funny-box">📂 تم رفع الملف بنجاح! الروبوت جاهز يذاكر عنك 🤖</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📝  Summary", "❓  Quiz"])

    with tab1:
        if st.button("✨  Generate Summary"):
            with st.spinner(random.choice(funny_loading)):
                summary = generate_summary(text)
            st.markdown(f'<div class="funny-box">{random.choice(funny_summary_done)}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="result-box">{summary}</div>', unsafe_allow_html=True)

    with tab2:
        if st.button("🎯  Generate Quiz"):
            with st.spinner(random.choice(funny_loading)):
                quiz = generate_quiz(text)
            st.markdown(f'<div class="funny-box">{funny_quiz_done}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="result-box">{quiz}</div>', unsafe_allow_html=True)

st.markdown('<div class="footer">🌿 جامعة الزيتونة للعلوم والتكنولوجيا | AI Study Assistant © 2026</div>', unsafe_allow_html=True)