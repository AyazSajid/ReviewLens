# app.py

import re
import streamlit as st
from pipeline import run_pipeline

st.set_page_config(
    page_title="ReviewLens - AI Review Analyzer",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------------------------
# Custom CSS
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&family=Inter:wght@400;500;600&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }

    .main {
        background: linear-gradient(180deg, #0f1117 0%, #171a23 100%);
    }

    .rl-hero {
        text-align: center;
        padding: 1.2rem 0 0.4rem 0;
    }

    .rl-hero h1 {
        font-family: 'Poppins', sans-serif;
        font-size: 2.6rem;
        font-weight: 700;
        background: linear-gradient(90deg, #7C5CFF, #35C6FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }

    .rl-hero p {
        color: #9aa1b2;
        font-size: 1.02rem;
        margin-top: 0;
    }

    div[data-testid="stTextInput"] input {
        background-color: #f5f6fa;
        border: 1px solid #d8dbe6;
        border-radius: 10px;
        color: #1c2030;
        padding: 0.7rem 1rem;
        font-size: 1rem;
    }

    div[data-testid="stTextInput"] input::placeholder {
        color: #8a8fa3;
    }

    div[data-testid="stTextInput"] input:focus {
        border: 1px solid #7C5CFF;
        box-shadow: 0 0 0 1px #7C5CFF;
    }

    div.stButton > button {
        background: linear-gradient(90deg, #7C5CFF, #35C6FF);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.65rem 1.6rem;
        font-weight: 600;
        font-size: 1rem;
        width: 100%;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }

    div.stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 18px rgba(124, 92, 255, 0.35);
        color: white;
    }

    .rl-card {
        background: #171b28;
        border: 1px solid #262b3d;
        border-radius: 16px;
        padding: 1.6rem 1.8rem;
        margin-top: 1.4rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.25);
    }

    .rl-card h3 {
        font-family: 'Poppins', sans-serif;
        margin-top: 0;
        font-size: 1.25rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .rl-badge {
        display: inline-block;
        padding: 0.3rem 0.9rem;
        border-radius: 999px;
        font-weight: 600;
        font-size: 0.95rem;
        margin-bottom: 0.8rem;
    }

    .rl-badge-good { background: rgba(52, 211, 153, 0.15); color: #34D399; border: 1px solid rgba(52,211,153,0.4);}
    .rl-badge-mid  { background: rgba(251, 191, 36, 0.15); color: #FBBF24; border: 1px solid rgba(251,191,36,0.4);}
    .rl-badge-low  { background: rgba(248, 113, 113, 0.15); color: #F87171; border: 1px solid rgba(248,113,113,0.4);}

    .rl-progress-track {
        background: #262b3d;
        border-radius: 999px;
        height: 12px;
        width: 100%;
        overflow: hidden;
        margin-top: 0.4rem;
    }

    .rl-progress-fill {
        height: 100%;
        border-radius: 999px;
        background: linear-gradient(90deg, #7C5CFF, #35C6FF);
    }

    .rl-footer {
        text-align: center;
        color: #6b7280;
        font-size: 0.85rem;
        margin-top: 2.5rem;
        padding-bottom: 1rem;
    }

    .rl-footer a { color: #9aa1b2; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------
st.markdown("""
<div class="rl-hero">
    <h1>🔍 ReviewLens</h1>
    <p>AI-powered product review summarizer &amp; bias auditor</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Input row
# ---------------------------------------------------------------------------
col1, col2 = st.columns([4, 1.3], vertical_alignment="bottom")
with col1:
    product_name = st.text_input(
        "Product name",
        placeholder="e.g., iPhone 17 Pro Max, boAt Airdopes 141...",
        label_visibility="collapsed"
    )
with col2:
    analyze_clicked = st.button("Analyze ✨")

# ---------------------------------------------------------------------------
# Helper: extract a bias score number from the bias report text
# ---------------------------------------------------------------------------
def extract_score(text: str):
    match = re.search(r"(\d{1,3})\s*/\s*100", text)
    if not match:
        match = re.search(r"Bias Score[:\s]*([0-9]{1,3})", text, re.IGNORECASE)
    if match:
        return min(int(match.group(1)), 100)
    return None


def badge_class(score: int) -> str:
    if score >= 75:
        return "rl-badge-good"
    elif score >= 45:
        return "rl-badge-mid"
    return "rl-badge-low"


# ---------------------------------------------------------------------------
# Run pipeline
# ---------------------------------------------------------------------------
if analyze_clicked:
    if not product_name.strip():
        st.warning("Please enter a product name first.")
    else:
        with st.spinner(f"Gathering reviews and analyzing '{product_name}'..."):
            try:
                result = run_pipeline(product_name)
            except Exception as e:
                result = None
                st.error(f"Something went wrong: {str(e)}")

        if result:
            # ---- Price Card ----
            st.markdown(f"""
            <div class="rl-card" style="text-align:center; padding: 1.2rem;">
                <p style="color:#9aa1b2; margin-bottom:0.2rem; font-size:0.9rem; letter-spacing:0.05em;">CURRENT PRICE</p>
                <h2 style="font-family:'Poppins',sans-serif; margin:0; color:#35C6FF;">{result['price']}</h2>
            </div>
            """, unsafe_allow_html=True)

            # ---- Summary Card ----
            st.markdown(f"""
            <div class="rl-card">
                <h3>📋 Review Summary — {product_name}</h3>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(result["summary"])

            # ---- Bias Card ----
            score = extract_score(result["bias_report"])
            st.markdown('<div class="rl-card">', unsafe_allow_html=True)
            st.markdown("### ⚖️ Bias Report")

            if score is not None:
                st.markdown(f"""
                    <span class="rl-badge {badge_class(score)}">Bias Score: {score}/100</span>
                    <div class="rl-progress-track">
                        <div class="rl-progress-fill" style="width:{score}%;"></div>
                    </div>
                    <br>
                """, unsafe_allow_html=True)

            st.markdown(result["bias_report"])
            st.markdown('</div>', unsafe_allow_html=True)

            # ---- Raw data ----
            with st.expander("🔎 View raw reviews used for this analysis"):
                st.text(result["raw_reviews"])

st.markdown("""
<div class="rl-footer">
    Built with LangChain • Groq • Tavily • Streamlit
</div>
""", unsafe_allow_html=True)