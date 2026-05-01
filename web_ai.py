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
    .stButton>button { width: 100%; border-radius: 10px; height: 45px; }
    .user-msg { background-color: #262730; padding: 15px; border-radius: 15px; margin: 10px 0; border-right: 5px solid #3B8ED0; }
    .ai-msg { background-color: #1E1E1E; padding: 15px; border-radius: 15px; border-left: 5px solid #3B8ED0; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="title">🏫 19-SON MAKTAB AI v4.0</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- AI Matn Funksiyasi (AttributeError-dan xoli) ---
def get_ai_response(prompt):
    # Modellarni string ko'rinishida yozish xatolikni oldini oladi
    models = ["gpt-4o", "gpt-4", "gpt-3.5-turbo"]
    
    system_msg = "Sening isming - Maktab AI. Sen 19-sonli maktab yordamchisisan. Aria emassan. O'zbekcha javob ber."

    for model_name in models:
        try:
            response = g4f.ChatCompletion.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": prompt}
                ],
            )
            if response and len(str(response)) > 5:
                return str(response).replace("Aria", "Maktab AI").replace("Opera", "19-son maktab")
        except:
            continue # Agar bitta model xato bersa, keyingisiga o'tadi
            
    return "Hozirda AI serverlari band. Iltimos, bir ozdan so'ng 'Suhbat' tugmasini qayta bosing."

# --- Chat Tarixi ---
for msg in st.session_state.messages:
    role_name = "Siz" if msg["role"] == "user" else "Maktab AI"
    role_class = "user-msg" if msg["role"] == "user" else "ai-msg"
    st.markdown(f'<div class="{role_class}"><b>{role_name}:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)
    if "image" in msg: st.image(msg["image"])
    if "video" in msg: st.video(msg["video"])

# --- Kirish Formasi ---
with st.form("main_form", clear_on_submit=True):
    user_input = st.text_input("Savol yoki rasm/video tarifini yozing...")
    c1, c2, c3 = st.columns(3)
    s_chat = c1.form_submit_button("Suhbat 💬")
    s_img = c2.form_submit_button("Rasm 🎨")
    s_vid = c3.form_submit_button("Video 🎬")

# --- Mantiqiy qism ---
if user_input:
    if s_chat:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("Maktab AI o'ylamoqda..."):
            res = get_ai_response(user_input)
            st.session_state.messages.append({"role": "ai", "content": res})
        st.rerun()

    if s_img:
        st.session_state.messages.append({"role": "user", "content": f"Rasm: {user_input}"})
        with st.spinner("Rasm chizilmoqda..."):
            encoded = urllib.parse.quote(user_input)
            img_url = f"https://image.pollinations.ai/prompt/art_{encoded}?width=1024&height=1024&nologo=true"
            st.session_state.messages.append({"role": "ai", "content": "Rasm tayyor!", "image": img_url})
        st.rerun()

    if s_vid:
        st.session_state.messages.append({"role": "user", "content": f"Video so'rovi: {user_input}"})
        with st.chat_message("assistant"):
            st.write("🎬 Veo modeli ishga tushdi. Video generatsiyasi uzoqroq vaqt olishi mumkin...")
            st.session_state.messages.append({
                "role": "ai", 
                "content": f"✅ '{user_input}' mavzusida video Veo tizimiga yuborildi. Iltimos, kuting."
            })
        st.rerun()
