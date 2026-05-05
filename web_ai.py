import streamlit as st
import g4f
import urllib.parse
import asyncio
import nest_asyncio

# Streamlit ichida asinxron funksiyalarni ishlatishga ruxsat berish
nest_asyncio.apply()

# Sahifa sozlamalari
st.set_page_config(page_title="19-son Maktab AI", page_icon="🏫")

# Dizayn
st.markdown("""
<style>
    .stApp { background-color: #121212; color: white; }
    .big-font { font-size: 25px !important; font-weight: bold; color: #3B8ED0; text-align: center; }
    .msg-box { padding: 10px; border-radius: 10px; margin-bottom: 10px; }
    .user { background-color: #262730; }
    .ai { background-color: #1E1E1E; border-left: 5px solid #3B8ED0; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font">🏫 19-SON MAKTAB AI YORDAMCHISI</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# AI dan javob olish funksiyasi
async def fetch_response(prompt):
    try:
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[
                {"role": "system", "content": "Sen 19-sonli maktab yordamchisisan. O'zbek tilida javob ber."},
                {"role": "user", "content": prompt}
            ]
        )
        return response
    except Exception as e:
        return f"Xatolik: {str(e)}"

# Tarixni ko'rsatish
for m in st.session_state.messages:
    cls = "user" if m["role"] == "user" else "ai"
    st.markdown(f'<div class="msg-box {cls}"><b>{m["role"].upper()}:</b><br>{m["content"]}</div>', unsafe_allow_html=True)
    if m.get("is_img"):
        st.image(m["content"])

# Kirish va tugmalar
user_input = st.text_input("Xabar yozing...", key="txt")
c1, c2 = st.columns(2)

if c1.button("Suhbat 💬") and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("AI o'ylamoqda..."):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        res = loop.run_until_complete(fetch_response(user_input))
        st.session_state.messages.append({"role": "ai", "content": res})
    st.rerun()

if c2.button("Rasm 🎨") and user_input:
    st.session_state.messages.append({"role": "user", "content": f"Rasm: {user_input}"})
    url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(user_input)}?nologo=true"
    st.session_state.messages.append({"role": "ai", "content": url, "is_img": True})
    st.rerun()
