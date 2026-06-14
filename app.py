import streamlit as st
from modules.pdf_extractor import extract_text_from_pdf
from modules.summarizer import generate_summary
from modules.quiz_generator import generate_quiz
from modules.chat_with_pdf import chat_with_pdf
from modules.mind_map import generate_mind_map_data
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
    .stApp {{ background: linear-gradient(160deg, #060f06 0%, #0f1f0f 40%, #060f06 100%); }}
    .main-header {{ text-align: center; padding: 2.5rem 1rem; background: linear-gradient(135deg, #0d1f0d, #1a3a1a); border-radius: 24px; border: 2px solid #c9a227; margin-bottom: 2rem; box-shadow: 0 0 40px rgba(201,162,39,0.25); }}
    .main-header img {{ width: 110px; margin-bottom: 1rem; filter: drop-shadow(0 0 12px rgba(201,162,39,0.5)); }}
    .main-header h1 {{ font-family: 'Playfair Display', serif; color: #c9a227; font-size: 2.8rem; font-weight: 900; margin: 0; letter-spacing: 2px; text-shadow: 0 0 25px rgba(201,162,39,0.6); }}
    .main-header .subtitle {{ color: #90c878; font-size: 1.05rem; margin-top: 0.5rem; letter-spacing: 1px; }}
    .welcome-banner {{ background: linear-gradient(135deg, #1a3314, #2a4a1a); border: 1px solid #c9a227; border-radius: 16px; padding: 1rem 2rem; text-align: center; color: #f5e6b0; font-size: 1.3rem; font-weight: 700; margin-bottom: 1.5rem; }}
    .funny-box {{ background: linear-gradient(135deg, #1a2e10, #243d18); border: 1px solid #c9a227; border-radius: 14px; padding: 0.9rem 1.5rem; margin: 1rem 0; color: #f5e6b0; font-size: 1.05rem; text-align: center; font-weight: 700; }}
    .result-box {{ background: linear-gradient(135deg, #0a1f0a, #102010); border: 1px solid #4a8a3a; border-radius: 16px; padding: 2rem; color: #dff0d8; line-height: 2; font-size: 1.05rem; }}
    .chat-box {{ background: linear-gradient(135deg, #0a1f0a, #102010); border: 1px solid #c9a227; border-radius: 16px; padding: 1.5rem; color: #dff0d8; line-height: 2; font-size: 1.05rem; margin-top: 1rem; }}
    .score-box {{ background: linear-gradient(135deg, #1a1a0a, #2a2a10); border: 2px solid #c9a227; border-radius: 16px; padding: 1.5rem; text-align: center; color: #f5e6b0; font-size: 1.5rem; font-weight: 900; margin: 1rem 0; }}
    .stButton > button {{ background: linear-gradient(135deg, #c9a227, #a07d1a) !important; color: #0a1a0a !important; font-family: 'Playfair Display', serif !important; font-weight: 700 !important; font-size: 1.1rem !important; border: none !important; border-radius: 12px !important; padding: 0.75rem 2rem !important; width: 100% !important; letter-spacing: 1px !important; transition: all 0.3s ease !important; }}
    .stButton > button:hover {{ transform: translateY(-3px) !important; box-shadow: 0 8px 25px rgba(201,162,39,0.5) !important; }}
    .stTabs [data-baseweb="tab-list"] {{ background: transparent !important; border-bottom: 2px solid #2a4a1a !important; }}
    .stTabs [data-baseweb="tab"] {{ color: #90c878 !important; font-weight: 700 !important; font-size: 1rem !important; letter-spacing: 1px !important; }}
    .stTabs [aria-selected="true"] {{ color: #c9a227 !important; border-bottom: 3px solid #c9a227 !important; }}
    .footer {{ text-align: center; color: #4a7a3a; padding: 1.5rem; margin-top: 2rem; border-top: 1px solid #2a4a1a; font-size: 0.9rem; letter-spacing: 1px; }}
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

if "score" not in st.session_state:
    st.session_state.score = 0
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.markdown(f"""
<div class="main-header">
    <img src="data:image/png;base64,{logo_base64}" alt="ZUST Logo"/>
    <h1>AI Study Assistant</h1>
    <div class="subtitle">جامعة الزيتونة للعلوم والتكنولوجيا</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="welcome-banner">
    🌿 ع قولة الدكتور بلال: يا هلااااااااا! أهلاً بك بمساعدك الذكي للدراسة 🌿
</div>
""", unsafe_allow_html=True)

st.markdown(f'<div class="score-box">🏆 نقاطك: {st.session_state.score}</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("📄 ارفع ملف PDF هون", type=["pdf"])

if uploaded_file:
    with st.spinner(random.choice(funny_loading)):
        text = extract_text_from_pdf(uploaded_file)
        text = chunk_text(text)

    st.markdown('<div class="funny-box">📂 تم رفع الملف بنجاح! الروبوت جاهز يذاكر عنك 🤖</div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["📝  Summary", "❓  Quiz", "💬  Chat with PDF", "🗺️  Mind Map"])

    with tab1:
        if st.button("✨  Generate Summary"):
            with st.spinner(random.choice(funny_loading)):
                summary = generate_summary(text)
            st.session_state.score += 10
            st.markdown(f'<div class="funny-box">{random.choice(funny_summary_done)}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="result-box">{summary}</div>', unsafe_allow_html=True)

    with tab2:
        if st.button("🎯  Generate Quiz"):
            with st.spinner(random.choice(funny_loading)):
                quiz = generate_quiz(text)
            st.session_state.score += 20
            st.markdown(f'<div class="funny-box">{funny_quiz_done}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="result-box">{quiz}</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown("### 💬 اسأل أي سؤال عن الـ PDF")
        question = st.text_input("اكتب سؤالك هون...")
        if st.button("🔍  Get Answer"):
            if question:
                with st.spinner("🤔 بفكر..."):
                    answer = chat_with_pdf(text, question)
                st.session_state.score += 5
                st.session_state.chat_history.append({"q": question, "a": answer})

        for chat in reversed(st.session_state.chat_history):
            st.markdown(f'<div class="chat-box">❓ <b>{chat["q"]}</b><br><br>💡 {chat["a"]}</div>', unsafe_allow_html=True)

    with tab4:
        if st.button("🗺️  Generate Mind Map"):
            with st.spinner("🧠 بنبني الخريطة الذهنية..."):
                mind_map_data = generate_mind_map_data(text)
            if mind_map_data:
                st.session_state.score += 15
                center = mind_map_data["center"]
                branches = mind_map_data["branches"]
                colors = ["#c9a227", "#4a8a3a", "#2a6a8a", "#8a2a6a"]
                positions = [(150, 120), (750, 120), (150, 480), (750, 480)]

                html = f"""
                <div style="background:#0a1f0a;border-radius:20px;padding:2rem;overflow-x:auto;">
                <svg width="900" height="600" viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
                <defs><filter id="glow"><feGaussianBlur stdDeviation="3" result="coloredBlur"/>
                <feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
                <ellipse cx="450" cy="300" rx="110" ry="55" fill="#1a3a1a" stroke="#c9a227" stroke-width="3" filter="url(#glow)"/>
                <text x="450" y="305" text-anchor="middle" fill="#c9a227" font-size="14" font-weight="bold" font-family="Arial">{center[:20]}</text>
                """

                for i, branch in enumerate(branches[:4]):
                    x, y = positions[i]
                    color = colors[i % len(colors)]
                    html += f"""
                    <line x1="450" y1="300" x2="{x}" y2="{y}" stroke="{color}" stroke-width="2" opacity="0.6"/>
                    <ellipse cx="{x}" cy="{y}" rx="90" ry="35" fill="#1a2a1a" stroke="{color}" stroke-width="2"/>
                    <text x="{x}" y="{y+5}" text-anchor="middle" fill="{color}" font-size="12" font-weight="bold" font-family="Arial">{branch['title'][:15]}</text>
                    """
                    child_positions = [(-130, -50), (-130, 0), (-130, 50)] if i % 2 == 0 else [(130, -50), (130, 0), (130, 50)]
                    for j, child in enumerate(branch.get('children', [])[:3]):
                        cx, cy = x + child_positions[j][0], y + child_positions[j][1]
                        html += f"""
                        <line x1="{x}" y1="{y}" x2="{cx}" y2="{cy}" stroke="{color}" stroke-width="1" opacity="0.4"/>
                        <rect x="{cx-60}" y="{cy-15}" width="120" height="30" rx="8" fill="#0f1f0f" stroke="{color}" stroke-width="1"/>
                        <text x="{cx}" y="{cy+5}" text-anchor="middle" fill="#dff0d8" font-size="10" font-family="Arial">{child[:18]}</text>
                        """

                html += "</svg></div>"
                st.markdown(f'<div class="funny-box">🗺️ الخريطة الذهنية جاهزة! +15 نقطة 🏆</div>', unsafe_allow_html=True)
                st.components.v1.html(html, height=650)

st.markdown('<div class="footer">🌿 جامعة الزيتونة للعلوم والتكنولوجيا | AI Study Assistant © 2026</div>', unsafe_allow_html=True)
