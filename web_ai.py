import streamlit as st
import g4f
import urllib.parse

# --- Sahifa sozlamalari ---
st.set_page_config(page_title="19-son Maktab AI", page_icon="🏫")

# --- Dizayn ---
st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: white; }
    .title { color: #3B8ED0; text-align: center; font-size: 30px; font-weight: bold; }
    .user-msg { background-color: #262730; padding: 10px; border-radius: 10px; margin: 5px 0; }
    .ai-msg { background-color: #1E1E1E; padding: 10px; border-radius: 10px; border-left: 5px solid #3B8ED0; margin: 5px 0; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="title">🏫 19-SON MAKTAB AI</p>', unsafe_allow_html=True)

# --- Xotira ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- AI Funksiyasi (Soddalashtirilgan) ---
def get_ai_response(prompt):
    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.default,
            messages=[
                {"role": "system", "content": "Sen 19-sonli maktab yordamchisisan. O'zbek tilida javob ber."},
                {"role": "user", "content": prompt}
            ],
        )
        return response
    except Exception as e:
        return "Xizmatda vaqtincha uzilish. Iltimos, birozdan so'ng urinib ko'ring."

# --- Chat tarixi ---
for msg in st.session_state.messages:
    role_class = "user-msg" if msg["role"] == "user" else "ai-msg"
    st.markdown(f'<div class="{role_class}"><b>{"Siz" if msg["role"] == "user" else "Maktab AI"}:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)
    if "image" in msg:
        st.image(msg["image"])

# --- Kirish maydoni ---
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Xabar yozing...")
    col1, col2 = st.columns(2)
    submit_chat = col1.form_submit_button("Suhbat 💬")
    submit_img = col2.form_submit_button("Rasm 🎨")

if submit_chat and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("O'ylamoqdaman..."):
        res = get_ai_response(user_input)
        st.session_state.messages.append({"role": "ai", "content": res})
    st.rerun()

if submit_img and user_input:
    st.session_state.messages.append({"role": "user", "content": f"Rasm: {user_input}"})
    with st.spinner("Chizilmoqda..."):
        encoded = urllib.parse.quote(user_input)
        img_url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&nologo=true"
        st.session_state.messages.append({"role": "ai", "content": "Marhamat, rasm tayyor!", "image": img_url})
    st.rerun()
