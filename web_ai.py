import streamlit as st
import g4f
import urllib.parse
import asyncio
import nest_asyncio

# Streamlit-da asinxron loop xatolarini tuzatish
nest_asyncio.apply()

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

# --- AI Javob Funksiyasi ---
async def fetch_ai_response(prompt):
    providers = [
        g4f.Provider.Blackbox,
        g4f.Provider.ChatGptEs,
        g4f.Provider.DuckDuckGo,
        g4f.Provider.Liaobots
    ]
    
    # MAKTAB MA'LUMOTLARI SHU YERDA:
    system_instructions = (
        "Sen Xorazm viloyati, Yangiariq tumani, Qo'riqtom qishlog'idagi 19-sonli maktabning rasmiy AI yordamchisisan. "
        "Maktab ma'lumotlari: \n"
        "- Manzil: Po'rsang mahallasi, Charog'bon ko'chasi 2-uy.\n"
        "- Tashkil etilgan: 02.09.1982.\n"
        "- Direktor: ESHMETOV RUSTAMBAY OLLABERGANOVICH.\n"
        "- O'qituvchilar: 65 ta. O'quvchilar: 570 ta.\n"
        "- Direktor o'rinbosarlari: Bekchanov Arslon, Jalilov Elbek, Salayev Mavlyanbek.\n"
        "- Aloqa: +998975156307.\n"
        "Sening isming - Maktab AI. Seni 19-son maktab jamoasi yaratgan. "
        "Faqat o'zbek tilida, muloyim javob ber."
    )

    for provider in providers:
        try:
            response = await g4f.ChatCompletion.create_async(
                model=g4f.models.gpt_4,
                provider=provider,
                messages=[
                    {"role": "system", "content": system_instructions},
                    {"role": "user", "content": prompt}
                ],
            )
            if response:
                return str(response).replace("Aria", "Maktab AI").replace("Opera", "19-son maktab")
        except:
            continue
            
    return "Hozirda serverlar band. Iltimos, bir ozdan so'ng urinib ko'ring."

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

# --- Suhbat logikasi ---
if submit_chat and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("Maktab AI o'ylamoqda..."):
        # Streamlit-da asinxron loopni to'g'ri ishga tushirish
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        answer = new_loop.run_until_complete(fetch_ai_response(user_input))
        st.session_state.messages.append({"role": "ai", "content": answer})
    st.rerun()

# --- Rasm logikasi ---
if submit_img and user_input:
    st.session_state.messages.append({"role": "user", "content": f"Rasm tarifi: {user_input}"})
    with st.spinner("Rasm tayyorlanmoqda..."):
        encoded_prompt = urllib.parse.quote(user_input)
        img_url = f"https://image.pollinations.ai/prompt/artistic_{encoded_prompt}?width=1024&height=1024&nologo=true"
        st.session_state.messages.append({
            "role": "ai", 
            "content": f"'{user_input}' asosida rasm chizildi:", 
            "image": img_url
        })
    st.rerun()
