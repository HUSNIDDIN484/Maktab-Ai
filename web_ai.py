import streamlit as st
import g4f
import urllib.parse
import asyncio
import nest_asyncio

# Streamlit-da asinxron (asyncio) muammolarni chetlab o'tish
try:
    nest_asyncio.apply()
except:
    pass

# --- Sahifa ko'rinishi ---
st.set_page_config(page_title="19-son Maktab AI", page_icon="🏫")

st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: white; }
    .header { font-size: 26px; font-weight: bold; color: #3B8ED0; text-align: center; }
    .chat-card { padding: 12px; border-radius: 10px; margin-bottom: 8px; border: 1px solid #333; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="header">🏫 19-SON MAKTAB AI TIZIMI</p>', unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- AI miyasidagi ma'lumotlar ---
async def get_ai_answer(user_msg):
    try:
        context = """
        Sen Yangiariq tumanidagi 19-sonli maktabning AI yordamchisisan.
        Maktab haqida faktlar:
        - Manzil: Qo'riqtom qishlog'i, Po'rsang mahallasi, Charog'bon ko'chasi 2-uy.
        - Direktor: ESHMETOV RUSTAMBAY OLLABERGANOVICH.
        - O'quvchilar: 570 ta. O'qituvchilar: 65 ta.
        - Tashkil etilgan: 02.09.1982.
        - Aloqa: +998975156307.
        - Rahbariyat: Bekchanov Arslon, Jalilov Elbek, Salayev Mavlyanbek.
        Har doim o'zbek tilida, do'stona javob ber.
        """
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": user_msg}
            ]
        )
        return response
    except Exception as e:
        return f"Xatolik: {str(e)}"

# --- Chat tarixi ---
for chat in st.session_state.chat_history:
    role = "Siz" if chat["role"] == "user" else "AI"
    st.markdown(f'<div class="chat-card"><b>{role}:</b><br>{chat["content"]}</div>', unsafe_allow_html=True)
    if "img" in chat:
        st.image(chat["img"])

# --- Buyruq kiritish ---
input_box = st.text_input("Savolingizni kiriting...", key="user_query")
c1, c2 = st.columns(2)

if c1.button("Suhbat 💬") and input_box:
    st.session_state.chat_history.append({"role": "user", "content": input_box})
    with st.spinner("AI javob bermoqda..."):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        reply = loop.run_until_complete(get_ai_answer(input_box))
        st.session_state.chat_history.append({"role": "ai", "content": reply})
    st.rerun()

if c2.button("Rasm 🎨") and input_box:
    st.session_state.chat_history.append({"role": "user", "content": f"Rasm: {input_box}"})
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(input_box)}?width=1024&height=1024&nologo=true"
    st.session_state.chat_history.append({"role": "ai", "content": "Tayyor!", "img": img_url})
    st.rerun()
