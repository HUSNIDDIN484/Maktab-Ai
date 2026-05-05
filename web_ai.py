import streamlit as st
import g4f
import urllib.parse
import asyncio
import nest_asyncio

# Asinxron xatoliklarni oldini olish
nest_asyncio.apply()

# --- Sahifa sozlamalari ---
st.set_page_config(page_title="19-son Maktab AI", page_icon="🏫", layout="centered")

# --- Dizayn (CSS) ---
st.markdown("""
<style>
    .stApp { background-color: #121212; color: white; }
    .big-font { font-size: 30px !important; font-weight: bold; color: #3B8ED0; text-align: center; }
    .user-msg { background-color: #262730; padding: 10px; border-radius: 10px; margin-bottom: 10px; }
    .ai-msg { background-color: #1E1E1E; padding: 10px; border-radius: 10px; border-left: 5px solid #3B8ED0; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font">🏫 19-SON MAKTAB AI YORDAMCHISI</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- AI funksiyasi ---
async def get_ai_response(prompt):
    try:
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
        return f"Xatolik: {str(e)}"

# --- Rasm funksiyasi ---
def generate_image_url(prompt):
    encoded_prompt = urllib.parse.quote(f"school style, {prompt}")
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"

# --- Suhbat tarixi ---
for msg in st.session_state.messages:
    role_class = "user-msg" if msg["role"] == "user" else "ai-msg"
    role_name = "Siz" if msg["role"] == "user" else "AI"
    st.markdown(f'<div class="{role_class}"><b>{role_name}:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)
    if msg.get("type") == "image":
        st.image(msg["content"], use_container_width=True)

# --- Kirish maydoni va tugmalar ---
user_input = st.text_input("Xabar yozing...", key="user_input")
col1, col2 = st.columns(2)

if col1.button("Suhbat 💬") and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("AI o'ylamoqda..."):
        response = asyncio.run(get_ai_response(user_input))
        st.session_state.messages.append({"role": "ai", "content": response})
    st.rerun()

if col2.button("Rasm 🎨") and user_input:
    st.session_state.messages.append({"role": "user", "content": f"Rasm so'rovi: {user_input}"})
    with st.spinner("Rasm chizilmoqda..."):
        img_url = generate_image_url(user_input)
        st.session_state.messages.append({"role": "ai", "content": "Mana siz so'ragan rasm:", "type": "image"})
        st.session_state.messages[-1]["content"] = img_url # Rasm linkini saqlash
    st.rerun()
