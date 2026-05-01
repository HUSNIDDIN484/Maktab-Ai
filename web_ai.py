import streamlit as st
import g4f
import urllib.parse

# --- Sahifa sozlamalari ---
st.set_page_config(
    page_title="19-son Maktab AI",
    page_icon="🏫",
    initial_sidebar_state="collapsed"
)

# --- Maxsus Dizayn (CSS) ---
st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: white; }
    .title { color: #3B8ED0; text-align: center; font-size: 32px; font-weight: bold; margin-bottom: 20px; text-shadow: 2px 2px 4px #000; }
    .user-msg { background-color: #262730; padding: 15px; border-radius: 15px; margin: 10px 0; border-right: 5px solid #3B8ED0; }
    .ai-msg { background-color: #1E1E1E; padding: 15px; border-radius: 15px; border-left: 5px solid #3B8ED0; margin: 10px 0; }
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="title">🏫 19-SON MAKTAB AI</p>', unsafe_allow_html=True)

# --- Xotira (Chat History) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- AI Javob Funksiyasi (Ko'p serverli tizim) ---
def get_ai_response(prompt):
    # Aria-dan qochish uchun bir nechta provayderlarni tekshiramiz
    providers = [
        g4f.Provider.Blackbox,
        g4f.Provider.ChatGptEs,
        g4f.Provider.Liaobots,
        g4f.Provider.DuckDuckGo
    ]
    
    system_instructions = (
        "Sening isming - Maktab AI. Sen 19-sonli maktab yordamchisisan. "
        "Seni 19-son maktab jamoasi yaratgan. O'zingni Aria yoki Opera deb tanishtirma. "
        "Faqat o'zbek tilida javob ber."
    )

    for provider in providers:
        try:
            response = g4f.ChatCompletion.create(
                model=g4f.models.gpt_4o,
                provider=provider,
                messages=[
                    {"role": "system", "content": system_instructions},
                    {"role": "user", "content": f"Sen 19-son maktab AIsan. Savol: {prompt}"}
                ],
            )
            if response and len(str(response)) > 5:
                # Aria yoki Opera so'zlarini tozalash
                clean_res = str(response).replace("Aria", "Maktab AI").replace("Opera", "19-son maktab")
                return clean_res
        except Exception:
            continue # Agar bitta provayder xato bersa, keyingisiga o'tadi
            
    return "Hozirda barcha AI serverlari band. Iltimos, 10 soniyadan so'ng yana bir bor urinib ko'ring."

# --- Chat tarixini ko'rsatish ---
for msg in st.session_state.messages:
    role_name = "Siz" if msg["role"] == "user" else "Maktab AI"
    role_class = "user-msg" if msg["role"] == "user" else "ai-msg"
    st.markdown(f'<div class="{role_class}"><b>{role_name}:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)
    if "image" in msg:
        st.image(msg["image"], use_container_width=True)

# --- Kiritish maydoni ---
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Savol yozing yoki rasm tarifini bering...")
    col1, col2 = st.columns(2)
    submit_chat = col1.form_submit_button("Suhbat 💬")
    submit_img = col2.form_submit_button("Rasm 🎨")

# --- Tugmalar bosilganda ---
if submit_chat and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("Maktab AI o'ylamoqda..."):
        answer = get_ai_response(user_input)
        st.session_state.messages.append({"role": "ai", "content": answer})
    st.rerun()

if submit_img and user_input:
    st.session_state.messages.append({"role": "user", "content": f"Rasm chizish: {user_input}"})
    with st.spinner("Rasm tayyorlanmoqda..."):
        encoded_prompt = urllib.parse.quote(user_input)
        # Pollinations - eng barqaror rasm generatori
        img_url = f"https://image.pollinations.ai/prompt/digital_art_style_{encoded_prompt}?width=1024&height=1024&nologo=true"
        st.session_state.messages.append({
            "role": "ai", 
            "content": f"'{user_input}' mavzusida rasm tayyorlandi!", 
            "image": img_url
        })
    st.rerun()
