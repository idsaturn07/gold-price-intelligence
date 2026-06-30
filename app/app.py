import streamlit as st
from model import get_gold_prediction, get_news_sentiment
from chatbot import ask_ai
import requests

# PAGE CONFIG
st.set_page_config(
    page_title="GoldPulse",
    page_icon="🪙",
    layout="wide"
)

# CUSTOM CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #0a0f1e 0%, #0d1b2a 50%, #0a0f1e 100%);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 2rem; }

.gold-header {
    background: linear-gradient(135deg, #0d1b2a, #1a2744);
    border: 1px solid #d4a843;
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.gold-header h1 { color: #d4a843; font-size: 2rem; font-weight: 700; margin: 0; letter-spacing: -0.5px; }
.gold-header p  { color: #8899aa; margin: 0.3rem 0 0; font-size: 0.9rem; }
.gold-badge {
    background: linear-gradient(135deg, #d4a843, #f0c060);
    color: #0a0f1e;
    padding: 0.4rem 1rem;
    border-radius: 20px;
    font-weight: 600;
    font-size: 0.85rem;
}

.metric-card {
    background: linear-gradient(135deg, #0d1b2a, #1a2744);
    border: 1px solid #1e3a5f;
    border-radius: 14px;
    padding: 1.5rem;
    text-align: center;
}
.metric-card:hover { border-color: #d4a843; }
.metric-label { color: #8899aa; font-size: 0.8rem; font-weight: 500; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.5rem; }
.metric-value { color: #d4a843; font-size: 1.8rem; font-weight: 700; line-height: 1; }
.metric-sub   { color: #5a7a9a; font-size: 0.75rem; margin-top: 0.3rem; }

.section-header {
    color: #d4a843;
    font-size: 1.1rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    padding: 0.5rem 0;
    border-bottom: 1px solid #1e3a5f;
    margin-bottom: 1rem;
}

.news-card {
    background: #0d1b2a;
    border: 1px solid #1e3a5f;
    border-left: 4px solid #d4a843;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
}
.news-card.positive { border-left-color: #2ecc71; }
.news-card.negative { border-left-color: #e74c3c; }
.news-card.neutral  { border-left-color: #3498db; }
.news-title { color: #c8d8e8; font-size: 0.9rem; font-weight: 500; text-decoration: none; }
.news-title:hover { color: #d4a843; }
.news-meta { display: flex; gap: 1rem; align-items: center; margin-top: 0.5rem; }
.sentiment-pill { padding: 0.2rem 0.7rem; border-radius: 20px; font-size: 0.75rem; font-weight: 600; }
.pill-positive { background: #1a3d2b; color: #2ecc71; }
.pill-negative { background: #3d1a1a; color: #e74c3c; }
.pill-neutral  { background: #1a2a3d; color: #3498db; }
.polarity-text { color: #5a7a9a; font-size: 0.8rem; }

.sentiment-banner { border-radius: 12px; padding: 1.2rem 1.5rem; margin: 1rem 0; display: flex; align-items: center; gap: 1rem; }
.banner-positive { background: #0d2a1a; border: 1px solid #2ecc71; }
.banner-negative { background: #2a0d0d; border: 1px solid #e74c3c; }
.banner-neutral  { background: #0d1a2a; border: 1px solid #3498db; }
.banner-icon { font-size: 1.8rem; }
.banner-text h3 { margin: 0; font-size: 1rem; font-weight: 600; }
.banner-text p  { margin: 0.2rem 0 0; font-size: 0.85rem; opacity: 0.8; }
.positive-text { color: #2ecc71; }
.negative-text { color: #e74c3c; }
.neutral-text  { color: #3498db; }

section[data-testid="stSidebar"] { background: #0d1b2a !important; border-right: 1px solid #1e3a5f; }

.stChatMessage { background: #0d1b2a !important; border: 1px solid #1e3a5f !important; border-radius: 12px !important; }
.stChatInputContainer { border-top: 1px solid #1e3a5f !important; background: #0a0f1e !important; }
.stChatInputContainer textarea {
    background: #0d1b2a !important;
    color: #c8d8e8 !important;
    border: 1px solid #1e3a5f !important;
    border-radius: 25px !important;
}
.stChatInputContainer textarea:focus { border-color: #d4a843 !important; }

.stButton button {
    background: transparent !important;
    border: 1px solid #1e3a5f !important;
    color: #8899aa !important;
    border-radius: 20px !important;
    font-size: 0.8rem !important;
}
.stButton button:hover { border-color: #e74c3c !important; color: #e74c3c !important; }
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0 1.5rem;'>
        <div style='font-size:2.5rem'>🪙</div>
        <div style='color:#d4a843; font-weight:700; font-size:1.1rem'>GoldPulse</div>
        <div style='color:#5a7a9a; font-size:0.8rem'>AI-Powered Market Analysis</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='color:#8899aa; font-size:0.75rem; text-transform:uppercase; letter-spacing:1px; margin-bottom:0.5rem'>Region</div>", unsafe_allow_html=True)
    country = st.selectbox("", ["Global", "India", "USA", "UK", "Japan"], label_visibility="collapsed")

    st.markdown("<hr style='border-color:#1e3a5f; margin: 1.5rem 0'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='background:#0a1628; border:1px solid #1e3a5f; border-radius:10px; padding:1rem; font-size:0.8rem'>
        <div style='color:#5a7a9a; margin-bottom:0.3rem'>Active Region</div>
        <div style='color:#d4a843; font-weight:600'>🌍 {country}</div>
    </div>
    """, unsafe_allow_html=True)

# ── HEADER ──
st.markdown(f"""
<div class="gold-header">
    <div>
        <h1>🪙 GoldPulse</h1>
        <p>AI-powered predictions · Live sentiment analysis · {country} market</p>
    </div>
    <div class="gold-badge">⚡ Live Analysis</div>
</div>
""", unsafe_allow_html=True)

# ── DISCLAIMER ──
st.info("⚠️ This tool is for informational purposes only and does not constitute financial advice. Always consult a professional before making investment decisions.")

# ── GET DATA ──
with st.spinner("⏳ Loading gold market data..."):
    try:
        df, prediction, mae, rmse = get_gold_prediction()
    except FileNotFoundError:
        st.error("❌ No trained model found!")
        st.info("👉 Run **`python model.py`** in your terminal first to train and save the model, then refresh this page.")
        st.stop()
    except Exception as e:
        st.error(f"❌ Error loading model: {e}")
        st.stop()

# ── CURRENCY SELECTOR ──
st.markdown("<div class='section-header'>💱 Select Currency</div>", unsafe_allow_html=True)

cur_col1, cur_col2, cur_col3, cur_col4, cur_col5 = st.columns(5)
currencies = ["USD", "INR", "EUR", "GBP", "JPY"]
currency_flags = {"USD": "🇺🇸 USD", "INR": "🇮🇳 INR", "EUR": "🇪🇺 EUR", "GBP": "🇬🇧 GBP", "JPY": "🇯🇵 JPY"}

if "currency" not in st.session_state:
    st.session_state.currency = "USD"

for col, cur in zip([cur_col1, cur_col2, cur_col3, cur_col4, cur_col5], currencies):
    with col:
        if st.button(currency_flags[cur], key=f"cur_{cur}", use_container_width=True):
            st.session_state.currency = cur
            st.rerun()

currency = st.session_state.currency
st.markdown("<br>", unsafe_allow_html=True)

# ── LIVE CURRENCY CONVERSION ──
@st.cache_data(ttl=3600)
def get_fx_rates():
    try:
        r = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=5)
        rates = r.json()["rates"]
        return {k: rates[k] for k in ["USD", "INR", "EUR", "GBP", "JPY"]}
    except Exception:
        return {"USD": 1, "INR": 83, "EUR": 0.92, "GBP": 0.78, "JPY": 150}

conversion_rates = get_fx_rates()
rate = conversion_rates[currency]
df_converted = df.copy()
df_converted['Close'] = df_converted['Close'] * rate
predicted_ounce_price = prediction * rate
price_per_gram = predicted_ounce_price / 28.3495

# ── DERIVED PRICES ──
price_per_kg   = price_per_gram * 1000
price_per_tola = price_per_gram * 11.6638
price_per_troy = predicted_ounce_price

# ── PRICE RANGE (using MAE as buffer) ──
price_low  = price_per_gram - (mae * rate / 28.3495)
price_high = price_per_gram + (mae * rate / 28.3495)

# ── METRIC CARDS — ROW 1: Prices ──
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Price per Gram</div>
        <div class="metric-value">{price_per_gram:.2f}</div>
        <div class="metric-sub">{currency} · Tomorrow's prediction</div>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Price per Troy Oz</div>
        <div class="metric-value">{price_per_troy:.0f}</div>
        <div class="metric-sub">{currency} · International standard</div>
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Price per Kg</div>
        <div class="metric-value">{price_per_kg:,.0f}</div>
        <div class="metric-sub">{currency} · Bulk / investment</div>
    </div>""", unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Price per Tola</div>
        <div class="metric-value">{price_per_tola:.2f}</div>
        <div class="metric-sub">{currency} · India / Middle East</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── PRICE RANGE BANNER ──
st.markdown(f"""
<div style='background: linear-gradient(135deg, #0d1b2a, #1a2744); border: 1px solid #1e3a5f;
     border-radius: 14px; padding: 1.2rem 2rem; display: flex; align-items: center;
     justify-content: space-between; flex-wrap: wrap; gap: 1rem;'>
    <div>
        <div style='color:#8899aa; font-size:0.75rem; text-transform:uppercase; letter-spacing:1px;'>
            Tomorrow's Predicted Price Range · {currency}
        </div>
        <div style='margin-top:0.4rem; font-size:0.85rem; color:#5a7a9a;'>
            Based on LSTM model prediction ± historical error margin
        </div>
    </div>
    <div style='display:flex; align-items:center; gap:1.5rem;'>
        <div style='text-align:center;'>
            <div style='color:#e74c3c; font-size:0.75rem; font-weight:600; text-transform:uppercase;'>Possible Low</div>
            <div style='color:#e74c3c; font-size:1.6rem; font-weight:700;'>{price_low:.2f}</div>
            <div style='color:#5a7a9a; font-size:0.72rem;'>{currency}/gram</div>
        </div>
        <div style='color:#3a5a7a; font-size:1.5rem;'>↔</div>
        <div style='text-align:center;'>
            <div style='color:#d4a843; font-size:0.75rem; font-weight:600; text-transform:uppercase;'>Predicted</div>
            <div style='color:#d4a843; font-size:1.6rem; font-weight:700;'>{price_per_gram:.2f}</div>
            <div style='color:#5a7a9a; font-size:0.72rem;'>{currency}/gram</div>
        </div>
        <div style='color:#3a5a7a; font-size:1.5rem;'>↔</div>
        <div style='text-align:center;'>
            <div style='color:#2ecc71; font-size:0.75rem; font-weight:600; text-transform:uppercase;'>Possible High</div>
            <div style='color:#2ecc71; font-size:1.6rem; font-weight:700;'>{price_high:.2f}</div>
            <div style='color:#5a7a9a; font-size:0.72rem;'>{currency}/gram</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── CHART + NEWS ──
left, right = st.columns([2, 1])

with left:
    st.markdown(f'<div class="section-header">📈 Gold Price Trend · {currency}</div>', unsafe_allow_html=True)
    st.line_chart(df_converted['Close'], color="#d4a843", height=280)
    st.caption("Source: Global gold futures (GC=F) · 5 year history")

with right:
    st.markdown('<div class="section-header">📰 Latest Gold News</div>', unsafe_allow_html=True)
    with st.spinner("Fetching latest news..."):
        articles, sentiments, polarities = get_news_sentiment(country)

    if articles:
        for i, (title, link) in enumerate(articles):
            s = sentiments[i].lower()
            st.markdown(f"""
            <div class="news-card {s}">
                <a href="{link}" target="_blank" class="news-title">📄 {title[:80]}{'...' if len(title) > 80 else ''}</a>
                <div class="news-meta">
                    <span class="sentiment-pill pill-{s}">{sentiments[i]}</span>
                    <span class="polarity-text">Polarity: {polarities[i]:.3f}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("<div style='color:#5a7a9a; font-size:0.9rem; padding:1rem'>No news available</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── OVERALL SENTIMENT ──
st.markdown('<div class="section-header">🌐 Overall Market Sentiment</div>', unsafe_allow_html=True)

if polarities and polarities != [0]:
    avg_polarity = sum(polarities) / len(polarities)
    if avg_polarity > 0.1:
        overall_sentiment = "Positive"
        st.markdown(f"""
        <div class="sentiment-banner banner-positive">
            <div class="banner-icon">📈</div>
            <div class="banner-text positive-text">
                <h3>Market Optimistic · Polarity {avg_polarity:.3f}</h3>
                <p>In {country}, positive sentiment may increase gold demand and drive prices higher.</p>
            </div>
        </div>""", unsafe_allow_html=True)
    elif avg_polarity < -0.1:
        overall_sentiment = "Negative"
        st.markdown(f"""
        <div class="sentiment-banner banner-negative">
            <div class="banner-icon">📉</div>
            <div class="banner-text negative-text">
                <h3>Market Risk · Polarity {avg_polarity:.3f}</h3>
                <p>In {country}, negative sentiment may reduce investor confidence in gold markets.</p>
            </div>
        </div>""", unsafe_allow_html=True)
    else:
        overall_sentiment = "Neutral"
        st.markdown(f"""
        <div class="sentiment-banner banner-neutral">
            <div class="banner-icon">⚖️</div>
            <div class="banner-text neutral-text">
                <h3>Market Stable · Polarity {avg_polarity:.3f}</h3>
                <p>In {country}, balanced sentiment indicates stable gold market conditions.</p>
            </div>
        </div>""", unsafe_allow_html=True)
else:
    overall_sentiment = "Neutral"
    st.markdown("""
    <div class="sentiment-banner banner-neutral">
        <div class="banner-icon">⚖️</div>
        <div class="banner-text neutral-text">
            <h3>No Data Available</h3>
            <p>Insufficient news data to determine market sentiment.</p>
        </div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── AI ASSISTANT ──
st.markdown('<div class="section-header">🤖 AI Gold Market Assistant</div>', unsafe_allow_html=True)

# ── SESSION STATE ──
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ── CLEAR BUTTON ──
if st.button("🗑 Clear Chat"):
    st.session_state.chat_history = []   # FIX: only clear chat, not entire session
    st.rerun()

# ── RENDER CHAT HISTORY ──
for msg in st.session_state.get("chat_history", []):
    if msg["role"] == "user":
        with st.chat_message("user", avatar="👤"):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant", avatar="🪙"):
            st.markdown(msg["content"])

# ── CHAT INPUT ──
user_input = st.chat_input(f"💬 Ask about gold market in {currency}...")

if user_input:
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar="🪙"):
        with st.spinner("🔍 Searching web & thinking..."):
            response = ask_ai(
                price_per_gram=price_per_gram,
                price_per_ounce=predicted_ounce_price,
                sentiment=overall_sentiment,
                question=user_input,
                country=country,
                currency=currency,
                history=st.session_state.chat_history
            )
        st.markdown(response)

    st.session_state.chat_history.append({"role": "user", "content": user_input})
    st.session_state.chat_history.append({"role": "assistant", "content": response})

# ── FOOTER ──
st.markdown("""
<div style='text-align:center; padding: 2rem 0 1rem; color:#2a4a6a; font-size:0.8rem; border-top:1px solid #1e3a5f; margin-top:2rem'>
    🪙 GoldPulse · Powered by Azure AI Foundry · LSTM Prediction Model
    <br><span style='color:#1a3a5a'>Data sourced from Yahoo Finance & NewsAPI · Not financial advice</span>
</div>
""", unsafe_allow_html=True)
