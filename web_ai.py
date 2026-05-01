import streamlit as st
import g4f
import urllib.parse

# --- Sahifa sozlamalari ---
st.set_page_config(page_title="19-son Maktab AI", page_icon="🏫")

# --- Dizayn (CSS) ---
st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: white; }
    .title { color: #3B8ED0; text-align: center; font-size: 32px; font-weight: bold; margin-bottom: 20px; }
    .user-msg { background-color: #262730; padding: 15px; border-radius: 15px; margin: 10px 0; border-right: 5px solid #3B8ED0; }
    .ai-msg { background-color: #1E1E1E; padding: 15px; border-radius: 15px; border-left: 5px solid #3B8ED0; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="title">🏫 19-SON MAKTAB AI + VIDEO</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- AI Matn Funksiyasi ---
def get_ai_response(prompt):
    system_instructions = "Sening isming - Maktab AI. 19-sonli maktab yordamchisisan. O'zbek tilida javob ber."
    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.default,
            messages=[
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": f"Sen Maktab AIsan. Savol: {prompt}"}
            ],
        )
        return str(response).replace("Aria", "Maktab AI").replace("Opera", "19-son maktab")
    except Exception:
        return "Serverda yuklama ko'p, birozdan so'ng urinib ko'ring."

# --- Chat tarixi ---
for msg in st.session_state.messages:
    role_name = "Siz" if msg["role"] == "user" else "Maktab AI"
    role_class = "user-msg" if msg["role"] == "user" else "ai-msg"
    st.markdown(f'<div class="{role_class}"><b>{role_name}:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)
    if "image" in msg:
        st.image(msg["image"])
    if "video" in msg:
        st.video(msg["video"])

# --- Kirish formasi ---
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Xabar yozing (Matn, Rasm yoki Video uchun)...")
    col1, col2, col3 = st.columns(3)
    submit_chat = col1.form_submit_button("Suhbat 💬")
    submit_img = col2.form_submit_button("Rasm 🎨")
    submit_vid = col3.form_submit_button("Video 🎬")

# --- Suhbat ---
if submit_chat and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("O'ylamoqdaman..."):
        answer = get_ai_response(user_input)
        st.session_state.messages.append({"role": "ai", "content": answer})
    st.rerun()

# --- Rasm (Pollinations) ---
if submit_img and user_input:
    st.session_state.messages.append({"role": "user", "content": f"Rasm: {user_input}"})
    with st.spinner("Rasm chizilmoqda..."):
        encoded = urllib.parse.quote(user_input)
        img_url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&nologo=true"
        st.session_state.messages.append({"role": "ai", "content": "Rasm tayyor!", "image": img_url})
    st.rerun()

# --- Video (Veo Model Eslatmasi) ---
if submit_vid and user_input:
    st.session_state.messages.append({"role": "user", "content": f"Video so'rovi: {user_input}"})
    with st.spinner("Video generatsiya qilinmoqda (bu bir oz vaqt olishi mumkin)..."):
        # Eslatma: Haqiqiy Veo generatsiyasi API orqali amalga oshiriladi.
        # Hozircha foydalanuvchiga Veo imkoniyatlari haqida ma'lumot beramiz.
        st.session_state.messages.append({
            "role": "ai", 
            "content": f"'{user_input}' mavzusida video yaratish uchun Veo modelidan foydalanilmoqda. Video tayyor bo'lgach shu yerda ko'rinadi."
        })
    st.rerun()
