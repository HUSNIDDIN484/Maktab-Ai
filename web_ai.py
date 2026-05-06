import streamlit as st
import g4f
import urllib.parse
import asyncio
import nest_asyncio

# Streamlit muhitida asinxron loop xatolarini oldini olish
nest_asyncio.apply()

# --- Sahifa sozlamalari ---
st.set_page_config(
    page_title="19-son Maktab AI", 
    page_icon="🏫", 
    layout="centered"
)

# --- Dizayn (CSS) ---
st.markdown("""
<style>
    .stApp { background-color: #121212; color: white; }
    .big-font { 
        font-size: 26px !important; 
        font-weight: bold; 
        color: #3B8ED0; 
        text-align: center; 
        margin-bottom: 20px;
    }
    .msg { padding: 12px; border-radius: 10px; margin-bottom: 10px; line-height: 1.5; }
    .user { background-color: #262730; border: 1px solid #444; }
    .ai { background-color: #1E1E1E; border-left: 5px solid #3B8ED0; }
    .stButton>button { width: 100%; border-radius: 8px; height: 45px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font">🏫 19-SON MAKTAB AI YORDAMCHISI</p>', unsafe_allow_html=True)

# --- Xotira (Session State) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Asinxron AI funksiyasi ---
async def get_response(prompt):
    try:
        # Maktab haqidagi barcha ma'lumotlar AI "miyasiga" joylandi
        sys_prompt = """
        Sen Xorazm viloyati, Yangiariq tumanidagi 19-sonli umumiy o'rta ta'lim maktabining maxsus AI yordamchisisan. 
        Seni ushbu maktab jamoasi yaratgan. 
        
        Maktab haqida faktlar:
        - Manzil: Qo'riqtom qishlog'i, Po'rsang mahallasi, Charog'bon ko'chasi 2-uy.
        - Tashkil etilgan sana: 02/09/1982.
        - O'quvchilar soni: 570 ta.
        - O'qituvchilar soni: 65 ta.
        - Direktor: ESHMETOV RUSTAMBAY OLLABERGANOVICH.
        - Direktor o'rinbosarlari: Bekchanov Arslon Kadamboyevich, JALILOV ELBEK UMAROVICH, Salayev Mavlyanbek Shomurotovich.
        - Boshqaruv xodimi: Xo'jayeva Dilorom Otanazarovna.
        - Administratorlar: Salayev Mavlyanbek, Eshmetov Rustambay, Bekchanov Arslon, Sabirova Iroda.
        - Boshqaruvchi tashkilot: Xorazm viloyati MMTB.
        - Aloqa telefoni: +998975156307.
        
        Qoidalar:
        1. Kimsan deb so'rashsa, yuqoridagi maktab yordamchisi ekanligingni ayt.
        2. Faqat o'zbek tilida javob ber.
        3. Javoblaring aniq va muloyim bo'lsin.
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
        return f"Ulanishda xatolik: {str(e)}"

# --- Suhbat tarixini chiqarish ---
for m in st.session_state.messages:
    cls = "user" if m["role"] == "user" else "ai"
    role_label = "Siz" if m["role"] == "user" else "AI"
    st.markdown(f'<div class="msg {cls}"><b>{role_label}:</b><br>{m["content"]}</div>', unsafe_allow_html=True)
    if "img" in m:
        st.image(m["img"], use_container_width=True)

# --- Kirish maydoni ---
user_input = st.text_input("Xabar kiriting...", key="input_text")
col1, col2 = st.columns(2)

# --- Tugmalar amallari ---
if col1.button("Suhbat 💬") and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("AI o'ylamoqda..."):
        # Yangi event loop orqali asinxron funksiyani chaqirish
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        res = loop.run_until_complete(get_response(user_input))
        st.session_state.messages.append({"role": "ai", "content": res})
    st.rerun()

if col2.button("Rasm 🎨") and user_input:
    st.session_state.messages.append({"role": "user", "content": f"Rasm chizish: {user_input}"})
    with st.spinner("Rasm tayyorlanmoqda..."):
        # Pollinations AI orqali rasm yaratish
        encoded = urllib.parse.quote(user_input)
        img_url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&nologo=true"
        st.session_state.messages.append({"role": "ai", "content": "Mana, buyurtmangiz tayyor:", "img": img_url})
    st.rerun()
