import streamlit as st
import g4f
import urllib.parse
import asyncio
import nest_asyncio

# Asinxron xatoliklarni oldini olish
nest_asyncio.apply()

# --- Sahifa sozlamalari ---
st.set_page_config(
    page_title="19-son Maktab AI",
    page_icon="🏫",
    layout="centered"
)

# --- Maxsus Dizayn (CSS) ---
st.markdown("""
<style>
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .main-title {
        font-size: 35px !important;
        font-weight: bold;
        color: #3B8ED0;
        text-align: center;
        text-shadow: 2px 2px 4px #000000;
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 50px;
        font-weight: bold;
        transition: 0.3s;
    }
    /* Suhbat tugmasi */
    div[data-testid="stHorizontalBlock"] > div:nth-child(1) .stButton>button {
        background-color: #3B8ED0;
        color: white;
        border: none;
    }
    /* Rasm tugmasi */
    div[data-testid="stHorizontalBlock"] > div:nth-color(2) .stButton>button {
        background-color: #A349A4;
        color: white;
        border: none;
    }
    .user-box {
        background-color: #262730;
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 10px;
        border: 1px solid #3B8ED0;
    }
    .ai-box {
        background-color: #1E1E1E;
        padding: 15px;
        border-radius: 15px;
        border-left: 6px solid #3B8ED0;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🏫 19-SON MAKTAB AI v3.0</p>', unsafe_allow_html=True)

# --- Xotira (Chat History) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- AI bilan bog'lanish (Matn) ---
async def get_ai_response(prompt):
    try:
        # AI o'zini Aria deb tanishtirmasligi uchun qat'iy ko'rsatma
        system_instructions = (
            "Sening isming 'Maktab AI'. Sen 19-sonli maktabning maxsus intellektual yordamchisisan. "
            "Seni 19-son maktab jamoasi yaratgan. O'zingni Aria yoki Opera deb tanishtirma. "
            "Faqat o'zbek tilida, do'stona va o'quvchilarga tushunarli tilda javob ber."
        )
        
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.gpt_4o,
            provider=g4f.Provider.Blackbox, # Barqaror provayder
            messages=[
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": prompt}
            ]
        )
        return response
    except Exception:
        return "Hozirda serverda yuklama ko'p. Iltimos, birozdan so'ng qayta urinib ko'ring."

# --- Rasm yaratish ---
def get_image_link(prompt):
    # Pollinations - eng tezkor rasm generatori
    encoded_text = urllib.parse.quote(f"digital art, high quality, school theme, {prompt}")
    return f"https://image.pollinations.ai/prompt/{encoded_text}?width=1024&height=1024&nologo=true"

# --- Chat interfeysi ---
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-box"><b>Siz:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)
    elif msg["role"] == "ai":
        st.markdown(f'<div class="ai-box"><b>Maktab AI:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)
    elif msg["role"] == "img":
        st.markdown(f'<div class="ai-box"><b>Maktab AI:</b><br>Rasm tayyor!</div>', unsafe_allow_html=True)
        st.image(msg["content"], use_container_width=True)

# Kiritish maydoni
input_text = st.text_input("Xabar yozing...", key="user_input")

col1, col2 = st.columns(2)

# --- Suhbat Harakati ---
if col1.button("Suhbat 💬") and input_text:
    st.session_state.messages.append({"role": "user", "content": input_text})
    
    with st.spinner("Maktab AI javob qaytarmoqda..."):
        answer = asyncio.run(get_ai_response(input_text))
        st.session_state.messages.append({"role": "ai", "content": answer})
    st.rerun()

# --- Rasm Harakati ---
if col2.button("Rasm 🎨") and input_text:
    st.session_state.messages.append({"role": "user", "content": f"Rasm chizish: {input_text}"})
    
    with st.spinner("Rasm chizilmoqda..."):
        img_url = get_image_link(input_text)
        st.session_state.messages.append({"role": "img", "content": img_url})
    st.rerun()

# Sahifa pastiga tushirish
st.markdown('<div id="end"></div>', unsafe_allow_html=True)
