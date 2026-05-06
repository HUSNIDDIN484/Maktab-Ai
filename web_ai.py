import streamlit as st
import g4f
import urllib.parse
import asyncio
import nest_asyncio

# Streamlit ichida asinxron loop xatoliklarini bartaraf etish
nest_asyncio.apply()

# --- Sahifa sozlamalari ---
st.set_page_config(page_title="19-son Maktab AI", page_icon="🏫")

# --- Dizayn (CSS) ---
st.markdown("""
<style>
    .stApp { background-color: #121212; color: white; }
    .big-font { font-size: 25px !important; font-weight: bold; color: #3B8ED0; text-align: center; }
    .msg { padding: 12px; border-radius: 10px; margin-bottom: 10px; }
    .user { background-color: #262730; border: 1px solid #444; }
    .ai { background-color: #1E1E1E; border-left: 5px solid #3B8ED0; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font">🏫 19-SON MAKTAB AI YORDAMCHISI</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Asinxron AI funksiyasi ---
async def get_response(prompt):
    try:
        # Maktab haqidagi ma'lumotlar AI bazasiga yuklandi
        sys_prompt = """
        Sen Xorazm viloyati, Yangiariq tumanidagi 19-sonli umumiy o'rta ta'lim maktabining maxsus AI yordamchisisan.
        Maktab ma'lumotlari:
        - Manzil: Qo'riqtom qishlog'i, Po'rsang mahallasi, Charog'bon ko'chasi 2-uy.
        - Tashkil etilgan sana: 02/09/1982.
        - O'quvchilar soni: 570 ta, O'qituvchilar soni: 65 ta.
        - Direktor: ESHMETOV RUSTAMBAY OLLABERGANOVICH.
        - Direktor o'rinbosarlari: Bekchanov Arslon, Jalilov Elbek, Salayev Mavlyanbek.
        - Aloqa: +998975156307.
        - Boshqaruvchi: Xorazm viloyati MMTB.
        
        Kimsan yoki maktab haqida so'ralganda faqat o'zbek tilida shu ma'lumotlar asosida javob ber.
        """
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        return response
    except Exception as e:
        return f"Xatolik yuz berdi: {str(e)}"

# --- Suhbat tarixini chiqarish ---
for m in st.session_state.messages:
    cls = "user" if m["role"] == "user" else "ai"
    st.markdown(f'<div class="msg {cls}"><b>{m["role"].upper()}:</b><br>{m["content"]}</div>', unsafe_allow_html=True)
    if "img" in m:
        st.image(m["img"])

# --- Kirish maydoni ---
user_input = st.text_input("Savolingizni yozing...", key="main_input")
col1, col2 = st.columns(2)

if col1.button("Suhbat 💬") and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("AI o'ylamoqda..."):
        # Yangi event loop orqali xatolikni cheklab o'tish
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        res = loop.run_until_complete(get_response(user_input))
        st.session_state.messages.append({"role": "ai", "content": res})
    st.rerun()

if col2.button("Rasm 🎨") and user_input:
    st.session_state.messages.append({"role": "user", "content": f"Rasm: {user_input}"})
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(user_input)}?width=1024&height=1024&nologo=true"
    st.session_state.messages.append({"role": "ai", "content": "Mana siz so'ragan rasm:", "img": img_url})
    st.rerun()
