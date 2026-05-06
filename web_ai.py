import streamlit as st
import g4f
import urllib.parse
import asyncio
import nest_asyncio

# Streamlit asinxron xatolarini cheklab o'tish
try:
    nest_asyncio.apply()
except:
    pass

# --- Sahifa sozlamalari ---
st.set_page_config(page_title="19-son Maktab AI", page_icon="🏫", layout="centered")

# --- Dizayn sozlamalari ---
st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    .main-title { font-size: 28px; font-weight: bold; color: #4A90E2; text-align: center; margin-bottom: 20px; }
    .chat-bubble { padding: 15px; border-radius: 15px; margin-bottom: 10px; border: 1px solid #30363D; }
    .user-msg { background-color: #161B22; }
    .ai-msg { background-color: #21262D; border-left: 5px solid #4A90E2; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🏫 19-SON MAKTAB AI YORDAMCHISI</div>', unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- AI miyasiga yuklangan ma'lumotlar ---
async def fetch_ai_response(user_query):
    try:
        system_instructions = """
        Sen Xorazm viloyati, Yangiariq tumanidagi 19-sonli umumiy o'rta ta'lim maktabining rasmiy AI yordamchisisan.
        Maktab pasporti:
        - Nomi: 19-sonli umumiy o'rta ta'lim maktabi.
        - Manzil: Qo'riqtom qishlog'i, Po'rsang mahallasi, Charog'bon ko'chasi 2-uy.
        - Tashkil topgan: 02.09.1982.
        - Kontingent: 570 o'quvchi va 65 o'qituvchi.
        - Direktor: ESHMETOV RUSTAMBAY OLLABERGANOVICH.
        - Rahbariyat: Bekchanov Arslon, Jalilov Elbek, Salayev Mavlyanbek (Direktor o'rinbosarlari).
        - Aloqa: +998975156307.
        - Yuqori tashkilot: Xorazm viloyati MMTB.
        
        Qoidalar: Har doim o'zbek tilida, muloyim va aniq javob ber. Kimsan desa, maktab yordamchisi ekaningni ayt.
        """
        
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": user_query}
            ]
        )
        return response
    except Exception as e:
        return f"Ulanishda xatolik: {str(e)}"

# --- Suhbat oynasi ---
for chat in st.session_state.chat_history:
    style_class = "user-msg" if chat["role"] == "user" else "ai-msg"
    st.markdown(f'<div class="chat-bubble {style_class}"><b>{chat["role"].upper()}:</b><br>{chat["content"]}</div>', unsafe_allow_html=True)
    if "image" in chat:
        st.image(chat["image"])

# --- Buyruqlar paneli ---
query = st.text_input("Savolingizni bu yerga yozing...", key="user_input")
btn_col1, btn_col2 = st.columns(2)

if btn_col1.button("Yuborish 📩") and query:
    st.session_state.chat_history.append({"role": "user", "content": query})
    with st.spinner("AI javob tayyorlamoqda..."):
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        ai_reply = new_loop.run_until_complete(fetch_ai_response(query))
        st.session_state.chat_history.append({"role": "ai", "content": ai_reply})
    st.rerun()

if btn_col2.button("Rasm yaratish 🖼️") and query:
    st.session_state.chat_history.append({"role": "user", "content": f"Rasm: {query}"})
    img_link = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(query)}?width=1024&height=1024&nologo=true"
    st.session_state.chat_history.append({"role": "ai", "content": "Siz so'ragan tasvir:", "image": img_link})
    st.rerun()
