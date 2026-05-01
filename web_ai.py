import streamlit as st
import g4f
import urllib.parse
import asyncio

# --- Sahifa sozlamalari ---
st.set_page_config(
    page_title="19-son Maktab AI",
    page_icon="🏫",
    layout="centered"
)

# --- Dizayn (CSS) ---
st.markdown("""
<style>
    .stApp {
        background-color: #121212;
        color: white;
    }
    .big-font {
        font-size: 30px !important;
        font-weight: bold;
        color: #3B8ED0;
        text-align: center;
    }
    .stButton>button {
        width: 100%;
        height: 50px;
        font-weight: bold;
    }
    /* Suhbat tugmasi */
    div[data-testid="stHorizontalBlock"] > div:nth-child(1) .stButton>button {
        background-color: #3B8ED0;
        color: white;
    }
    /* Rasm tugmasi */
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) .stButton>button {
        background-color: #A349A4;
        color: white;
    }
    .user-msg {
        background-color: #262730;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .ai-msg {
        background-color: #1E1E1E;
        padding: 10px;
        border-radius: 10px;
        border-left: 5px solid #3B8ED0;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# sarlavha
st.markdown('<p class="big-font">🏫 19-SON MAKTAB AI YORDAMCHISI</p>', unsafe_allow_html=True)

# --- Chat tarixini saqlash ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Asinxron chat funksiyasi ---
async def get_ai_response(prompt):
    try:
        # Tizim ko'rsatmasi
        system_msg = "Sen 19-sonli maktab yordamchisisan. Seni 19-son maktab jamoasi yaratgan. O'zbek tilida javob ber."
        
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt}
            ]
        )
        return response
    except Exception as e:
        return f"Xatolik yuz berdi: {str(e)}"

# --- Rasm yaratish funksiyasi ---
def generate_image_url(prompt):
    # Pollinations AI orqali tezkor link yaratish
    encoded_prompt = urllib.parse.quote(f"school style, {prompt}")
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"
    return image_url

# --- Interfeys elementlari ---

# Eski xabarlarni ko'rsatish
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-msg"><b>Siz:</b><br>{message["content"]}</div>', unsafe_allow_html=True)
    elif message["role"] == "ai":
        st.markdown(f'<div class="ai-msg"><b>AI:</b><br>{message["content"]}</div>', unsafe_allow_html=True)
    elif message["role"] == "image":
        st.markdown(f'<div class="ai-msg"><b>AI (Rasm):</b><br><a href="{message["content"]}" target="_blank">Rasmni ko\'rish uchun bu yerni bosing</a></div>', unsafe_allow_html=True)
        st.image(message["content"], use_container_width=True)

# Matn kiritish maydoni
user_input = st.text_input("Savolingizni yoki rasm tarifini yozing...", key="input")

# Tugmalar uchun ustunlar
col1, col2 = st.columns(2)

# --- Tugmalar bosilgandagi harakatlar ---

# 1. Suhbat tugmasi
if col1.button("Suhbat 💬") and user_input:
    # Foydalanuvchi xabarini saqlash
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(f'<div class="user-msg"><b>Siz:</b><br>{user_input}</div>', unsafe_allow_html=True)
    
    with st.spinner("AI o'ylamoqda..."):
        # AI javobini olish
        response = asyncio.run(get_ai_response(user_input))
        st.session_state.messages.append({"role": "ai", "content": response})
        st.markdown(f'<div class="ai-msg"><b>AI:</b><br>{response}</div>', unsafe_allow_html=True)
    
    # Kiritish maydonini tozalash uchun sahifani yangilash
    st.rerun()

# 2. Rasm tugmasi
if col2.button("Rasm 🎨") and user_input:
    # Foydalanuvchi xabarini saqlash
    st.session_state.messages.append({"role": "user", "content": f"Rasm: {user_input}"})
    st.markdown(f'<div class="user-msg"><b>Siz:</b><br>Rasm: {user_input}</div>', unsafe_allow_html=True)
    
    with st.spinner("Rasm chizilmoqda..."):
        # Rasm linkini yaratish
        image_url = generate_image_url(user_input)
        st.session_state.messages.append({"role": "image", "content": image_url})
        st.markdown(f'<div class="ai-msg"><b>AI (Rasm):</b><br><a href="{image_url}" target="_blank">Rasmni ko\'rish uchun bu yerni bosing</a></div>', unsafe_allow_html=True)
        st.image(image_url, use_container_width=True)
    
    st.rerun()
